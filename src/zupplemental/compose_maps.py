# compose_maps.py
# make ALL the maps

import math
import re

from generate_political_shapes import plot_political_shapes
from generate_graticule import generate_graticule, generate_backdrop
from generate_indicatrices import generate_indicatrices
from generate_orthodromes import generate_orthodromes
from generate_shapes import plot_shapes
from generate_labels import generate_topographical_labels, label_shapes, label_points


def main():
	# landmasses
	write_svg_code_to_file(
		"../../input/Basic.svg",
		'	<g transform="matrix(1,0,0,-1,180,90)">\n'
		'		<g class="land">\n'
		+ plot_shapes('ne_50m_land', trim_antarctica=True, mark_antarctica=True) +
		'		</g>\n'
		'		<g class="water">\n'
		+ plot_shapes('ne_50m_lakes', max_rank=4) +
		'		</g>\n'
		'	</g>\n'
	)

	# graticule
	write_svg_code_to_file(
		"../../input/Graticule.svg",
		'	<g transform="matrix(1,0,0,-1,180,90)">\n'
		'		<g class="graticule">\n'
		+ generate_graticule(5, 1, include_tropics=True, adjust_poles=True) +
		'		</g>\n'
		'	</g>\n'
	)

	# graticule2
	write_svg_code_to_file(
		"../../input/Graticule.svg",
		'	<g transform="matrix(1,0,0,-1,180,90)">\n'
		'		<g class="graticule">\n'
		+ generate_graticule(5, 1, include_tropics=True, adjust_poles=True, double_dateline=True) +
		'		</g>\n'
		'	</g>\n'
	)

	# compound
	write_svg_code_to_file(
		"../../input/Compound.svg",
		'	<rect class="water" width="100%" height="100%" />\n'
		'	<g transform="matrix(1,0,0,-1,180,90)">\n'
		'		<g class="land">\n'
		+ plot_shapes('ne_50m_land', trim_antarctica=True, mark_antarctica=True) +
		'		</g>\n'
		'		<g class="river">\n'
		+ plot_shapes('ne_50m_rivers_lake_centerlines', max_rank=4) +
		'		</g>\n'
		'		<g class="lakes">\n'
		+ plot_shapes('ne_50m_lakes', max_rank=4) +
		'		</g>\n'
		'		<g class="graticule">\n'
		+ generate_graticule(15, 1, include_tropics=True, adjust_poles=True) +
		'		</g>\n'
		'	</g>\n'
	)

	# indicatrices
	write_svg_code_to_file(
		"../../input/Tissot.svg",
		'	<rect class="water" width="100%" height="100%" />\n'
		'	<g transform="matrix(1,0,0,-1,180,90)">\n'
		'		<g class="land">\n'
		+ plot_shapes('ne_50m_land', trim_antarctica=True) +
		'		</g>\n'
		'		<g class="lakes">\n'
		+ plot_shapes('ne_50m_lakes', max_rank=4) +
		'		</g>\n'
		'		<g class="tissot">\n'
		+ generate_indicatrices(15, math.radians(3.75), resolution=180, adjust_poles=True) +
		'		</g>\n'
		'	</g>\n'
	)

	# indicatrices2
	for ctr_meridian in [+0, -20]:
		write_svg_code_to_file(
			f"../../input/Advanced/Tissot Wikipedia {ctr_meridian:+.0f}.svg",
			'	<g transform="matrix(1,0,0,-1,180,90)">\n'
			'		<g class="water">\n'
			+ generate_backdrop(.5, ctr_meridian=ctr_meridian) +
			'		</g>\n'
			'		<g class="land">\n'
			+ plot_shapes('ne_110m_land', flesh_out_antarctica=True) +
			'		</g>\n'
			'		<g class="lakes">\n'
			+ plot_shapes('ne_110m_lakes') +
			'		</g>\n'
			'		<g class="graticule">\n'
			+ generate_graticule(10, .5, double_dateline=(ctr_meridian == 0)) +
			'		</g>\n'
			'		<g class="tissot">\n'
			+ generate_indicatrices(30, 500/6371, ctr_meridian=ctr_meridian,
			                        adjust_poles=True, resolution=120, side_res=5, pole_res=120) +
			'		</g>\n'
			'	</g>\n'
		)

	# political
	write_svg_code_to_file(
		"../../input/Political.svg",
		'	<g transform="matrix(1,0,0,-1,180,90)">\n'
		'		<g class="country">\n'
		+ plot_political_shapes('ne_50m_admin_0_countries', trim_antarctica=True, mode="polygon") +
		'		</g>\n'
		'		<g class="lakes">\n'
		+ plot_shapes('ne_50m_lakes', max_rank=4) +
		'		</g>\n'
		'		<g class="country">\n'
		+ plot_political_shapes('ne_50m_admin_0_countries', trim_antarctica=True, mode="circle") +
		'		</g>\n'
		'	</g>\n'
		+ label_shapes('ne_50m_admin_0_countries', "pol", secondary_attr="NOTE_ADM0")
	)

	# fine_political
	write_svg_code_to_file(
		"../../input/Advanced/Fine political.svg",
		'	<g transform="matrix(1,0,0,-1,180,90)">\n'
		'		<g class="country">\n'
		+ plot_shapes('ne_50m_admin_0_countries', trim_antarctica=True) +
		'		</g>\n'
		'		<g class="province">\n'
		+ plot_shapes('ne_50m_admin_1_states_provinces', trim_antarctica=True) +
		'		</g>\n'
		'		<g class="lakes">\n'
		+ plot_shapes('ne_50m_lakes', max_rank=4) +
		'		</g>\n'
		'	</g>\n'
	)

	# orthodromes
	write_svg_code_to_file(
		"../../input/Orthodromes.svg",
		'	<g transform="matrix(1,0,0,-1,180,90)">\n'
		'		<g class="lines">\n'
		+ generate_orthodromes() +
		'		</g>\n'
		'	</g>\n'
	)

	# everything
	write_svg_code_to_file(
		"../../input/Advanced/Supermap.svg",
		'<rect class="water" width="100%" height="100%" />\n'
		'	<g transform="matrix(1,0,0,-1,180,90)">\n'
		'		<g class="country">\n'
		+ plot_political_shapes('ne_10m_admin_0_countries', trim_antarctica=True, mode="polygon") +
		'		</g>\n'
		'		<g class="thick-country-border">\n'
		+ plot_political_shapes('ne_10m_admin_0_countries', trim_antarctica=True, mode="border") +
		'		</g>\n'
		'		<g class="country-border">\n'
		+ plot_shapes('ne_10m_admin_0_map_units') +
		'		</g>\n'
		'		<g class="province-border">\n'
		+ plot_shapes('ne_10m_admin_1_states_provinces_lines', filter_field='ADM0_A3',
		              filter_values=['RUS', 'CAN', 'CHN', 'USA', 'BRA', 'AUS', 'IND', 'ARG', 'KAZ']) +
		'		</g>\n'
		'		<g class="disputed-border">\n'
		+ plot_shapes('ne_10m_admin_0_boundary_lines_disputed_areas') +
		'		</g>\n'
		'		<g class="coastline">\n'
		+ plot_shapes('ne_10m_coastline', trim_antarctica=True) +
		'		</g>\n'
		'		<g class="river">\n'
		+ plot_shapes('ne_10m_rivers_lake_centerlines', max_rank=5) +
		'		</g>\n'
		'		<g class="lake">\n'
		+ plot_shapes('ne_10m_lakes', max_rank=4) +
		'		</g>\n'
		'		<g class="graticule">\n'
		+ generate_graticule(5, 1, include_tropics=True, adjust_poles=True)
		+ plot_shapes('ne_10m_geographic_lines', clazz="dateline", filter_field='name',
		              filter_values=["International Date Line"]) +
		'		</g>\n'
		'	</g>\n'
		+ generate_topographical_labels('ne_50m', max_rank=2, text_size=4)
		+ label_shapes('ne_10m_lakes', "sea", max_rank=1, text_size=1)
		+ label_shapes('ne_10m_admin_0_countries', "pol", text_size=4, secondary_attr="NOTE_ADM0")
		+ label_points('ne_50m_populated_places_simple', "cit", text_size=0, max_rank=3)
	)


def write_svg_code_to_file(filename: str, code: str) -> None:
	with open(filename, "r", encoding="utf-8") as file:
		original_text = file.read()
	original_text = re.sub(r"\r\n?", "\n", original_text)
	header = re.search(r"^.*</style>\n", original_text, re.DOTALL).group()
	footer = "</svg>\n"
	new_text = header + code + footer
	with open(filename, "w", encoding="utf-8") as file:
		file.write(new_text)
	print(f"saved '{filename}'")


if __name__ == '__main__':
	main()
