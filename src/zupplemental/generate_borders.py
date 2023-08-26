import shapefile
from numpy import pi, sqrt
from shapefile import ShapeRecord
from shapely import Polygon

from helpers import plot, trim_edges

SIZE_CLASSES = ['lg', 'md', 'sm', None, None, None]
CIRCLE_RADIUS = 10


def generate_borders(source, borders_only=False, trim_antarctica=False, add_circles=False):
	"""data from https://www.naturalearthdata.com/"""
	sf = shapefile.Reader("shapefiles/{}_admin_0_countries".format(source))

	# first sort records into a dictionary by admin0 A3 code
	sovereignties: dict[str, list[ShapeRecord]] = {}
	for region in sf.shapeRecords():
		if trim_antarctica:
			if region.record.SOV_A3 == 'ATA':  # if it is Antarctica, trim it
				region.shape.points = trim_edges(region.shape.points, region.shape.parts)
		sovereignties[region.record.SOV_A3] = sovereignties.get(region.record.SOV_A3, []) + [region]

	# next, go thru and plot the borders
	for sovereignty_code, regions in sorted(sovereignties.items()):
		sovereign_code = complete_sovereign_code_if_necessary(sovereignty_code, regions)
		print(f'\t\t\t<g id="{sovereign_code}">')
		for region in regions:
			region_code = region.record.ADM0_A3
			is_sovereign = region_code == sovereign_code
			if is_sovereign:
				region_code = f"{region_code}_"  # add a suffix because ids have to be unique
			if borders_only:
				print(f'\t\t\t\t<clipPath id="{region_code}-clipPath">')
				print(f'\t\t\t\t\t<use href="#{region_code}" />')
				print(f'\t\t\t\t</clipPath>')
				print(f'\t\t\t\t<use href="#{region_code}" style="fill:none; clip-path:url(#{region_code}-clipPath);" />')
			else:
				plot(region.shape.points, midx=region.shape.parts, close=False,
				     fourmat='xd', tabs=4, ident=region_code)

			if add_circles:
				too_small = True
				for i in range(len(region.shape.parts)):
					if i + 1 < len(region.shape.parts):
						part = region.shape.points[region.shape.parts[i]:region.shape.parts[i + 1]]
					else:
						part = region.shape.points[region.shape.parts[i]:]
					# if Polygon(part).buffer(-CIRCLE_RADIUS).area == 0:
					if Polygon(part).area < pi*CIRCLE_RADIUS**2:
						too_small = False
				if too_small:
					capital_λ, capital_ф = float(region.record.LABEL_X), float(region.record.LABEL_Y)
					if is_sovereign:
						radius = CIRCLE_RADIUS
					else:
						radius = CIRCLE_RADIUS/sqrt(2)
					print(f'\t\t\t\t<circle x="{capital_λ}" y="{capital_ф}" r="{radius} />')
		print('\t\t\t</g>')


def complete_sovereign_code_if_necessary(sovereignty_code: str, regions: list[ShapeRecord]) -> str:
	""" so, under the NaturalEarth dataset system, countries are grouped together under
	    sovereignties.  and each sovereignty has one country within it which is in charge.  let's call it
	    the sovereign.  to encode this, the dataset gives every region a sovereign code and an admin0 code,
	    where the admin0 code is from some ISO standard, and the sovereign code = if it's the only region
	    under this sovereign { the admin0 code } else { the admin0 code of the sovereign with its last
	    letter replaced with a 1 };  I find this kind of weird; I can't find any basis for it in ISO
	    standards.  I get it, but I would rather the sovereign code just be the same as the admin0 code of
	    the sovereign.  so that's what this function does; it figures out what letter should go where that
	    1 is.
	"""
	sovereign_code = None
	for region in regions:
		if region.record.ADM0_A3[:2] == sovereignty_code[:2]:
			if sovereign_code is not None:
				raise ValueError(f"there are two possible sovereign codes for {sovereignty_code} and I "
				                 f"don't know which to use: {sovereign_code} and {region.record.ADM0_A3}")
			else:
				sovereign_code = region.record.ADM0_A3
	if sovereign_code is None:
		raise ValueError(f"there are no possible sovereign codes for {sovereignty_code}")
	return sovereign_code
