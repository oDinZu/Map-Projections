/**
 * MIT License
 * 
 * Copyright (c) 2017 Justin Kunimune
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */
package maps;

import de.jtem.mfc.field.Complex;
import maps.Projection.Property;
import maps.Projection.Type;

/**
 * A map optimised specifically for the 50 united states of America.
 * Source: 
 * Snyder, John Parr (1985). "Computer-assisted map projection research". Bulletin. United States
 *     Geological Survey. 1629: 79�92; 147�51.
 * 
 * @author jkunimune
 */
public class Snyder {
	
	private static final double[] POLE = { Math.PI/4, -2*Math.PI/3, 0 };
	private static final double[] A = {
			 0.05,  0.9842990,  0.0211642, -0.1036018, -0.0329095,  0.0499471,  0.0260460,
			        0.0007388,  0.0075848, -0.0216473, -0.0225161 }; //the real components of the coefficients
	private static final double[] B = {
			-0.07,  0.,         0.0037608, -0.0575102, -0.0320119,  0.1223335,  0.0899805,
			       -0.1435792, -0.1334108,  0.0776645,  0.0853673 }; //the imaginary components of the coefficients
	
	private static final double TOLERANCE = 1e-4;
	private static final double[] LIMS = {
			Math.toRadians(10), Math.toRadians(90), Math.toRadians(-195), Math.toRadians(-50) }; //trims the outside unsightly portions
	
	
	public static final Projection GS50 =
			new Projection(
					"GS50", "'MURKA!", 1.6, 1.1, 0b0011, Type.POLYNOMIAL, Property.CONFORMAL, 3,
					new String[] {}, new double[][] {}, false) {
		
		public double[] project(double lat, double lon) {
			if (lat < LIMS[0]) 	lat = LIMS[0]; //cut out the farther more unsightly bits
			if (lat > LIMS[1]) 	lat = LIMS[1];
			if (lon > 0 && lon-2*Math.PI < LIMS[2]) 	lon = LIMS[2];
			if (lon < 0 && lon > LIMS[3]) 	lon = LIMS[3];
			
			final double g = Math.sin(lat)*Math.sin(POLE[0]) + Math.cos(lat)*Math.cos(POLE[0])*Math.cos(lon-POLE[1]);
			final double s = 2/(1+g);
			final Complex z = new Complex(s*Math.cos(lat)*Math.sin(lon-POLE[1]), s*(Math.sin(lat)*Math.cos(POLE[0]) - Math.cos(lat)*Math.sin(POLE[0])*Math.cos(lon-POLE[1])));
			final Complex p = f(z);
			return new double[] { p.getRe(), p.getIm() };
		}
		
		public double[] inverse(double x, double y) {
			final Complex p = new Complex(x, y);
			Complex z = p; //initial guess
			Complex error = f(z).minus(p);
			for (int i = 0; error.abs() > TOLERANCE; i ++) {
				if (i == 9) 	return null;
				final Complex deriv = fp(z);
				z = z.minus(error.divide(deriv));
				error = f(z).minus(p);
			}
			double r = z.abs();
			double phi = 2*Math.atan(r/2);
			double lat = Math.asin(Math.cos(phi)*Math.sin(POLE[0]) + z.getIm()*Math.sin(phi)*Math.cos(POLE[0])/r);
			double lon = POLE[1] + Math.atan(z.getRe()*Math.sin(phi)/(r*Math.cos(POLE[0])*Math.cos(phi)-z.getIm()*Math.sin(POLE[0]*Math.sin(phi))));
			if (lat < LIMS[0] || lat > LIMS[1]) 	return null;
			if (lon < LIMS[2] || lon > LIMS[3]) 	return null;
			if (lon < -Math.PI) 	lon += 2*Math.PI;
			return new double[] {lat, lon};
		}
		
		@Override
		public double[] project(double lat, double lon, double[] pole) {
			return super.project(lat, lon, null);
		}
		
		@Override
		public double[] inverse(double x, double y, double[] pole, boolean crop) {
			return super.inverse(x, y, null, crop);
		}
	};
	
	
	private static final Complex f(Complex z) {
		Complex p = new Complex();
		for (int k = A.length-1; k >= 0; k --) {
			p = p.times(z).plus(new Complex(A[k], B[k]));
		}
		return p;
	}
	
	
	private static final Complex fp(Complex z) {
		Complex p = new Complex();
		for (int k = A.length-1; k > 0; k --) {
			p = p.times(z).plus(new Complex(A[k], B[k]).times(k));
		}
		return p;
	}
	
}
