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

import maps.Projection.Property;
import maps.Projection.Type;
import utils.Shape;

import static java.lang.Math.PI;
import static java.lang.Math.asin;
import static java.lang.Math.atan;
import static java.lang.Math.cos;
import static java.lang.Math.log;
import static java.lang.Math.pow;
import static java.lang.Math.sin;
import static java.lang.Math.sinh;
import static java.lang.Math.sqrt;
import static java.lang.Math.tan;
import static java.lang.Math.toRadians;

/**
 * Map projections where x is a linear function of longitude.
 * 
 * @author jkunimune
 */
public class Cylindrical {
	
	public static final Projection MERCATOR = new Projection(
			"Mercator", Shape.rectangle(2*PI, 2*PI), 0b0111, Type.CYLINDRICAL, Property.CONFORMAL, 1,
			"very popular") {
		
		public double[] project(double lat, double lon) {
			return new double[] {lon, log(tan(PI/4+lat/2))};
		}
		
		public double[] inverse(double x, double y) {
			return new double[] {atan(sinh(y)), x};
		}
	};
	
	
	public static final Projection PLATE_CARREE = new Projection(
			"Plate Carr\u00E9e", Shape.rectangle(2*Math.PI, Math.PI), 0b1111, Type.CYLINDRICAL,
			Property.EQUIDISTANT, 2, null, "focused on the equator"){
		
		public double[] project(double lat, double lon) {
			return new double[] {lon, lat};
		}
		
		public double[] inverse(double x, double y) {
			return new double[] {y, x};
		}
	};
	
	
	public static final Projection EQUIRECTANGULAR = new Projection(
			"Equirectangular", "A linear mapping from longitude and latitude to x and y.",
			null, 0b1111, Type.CYLINDRICAL, Property.EQUIDISTANT, 2,
			new String[]{"Std. parallel"}, new double[][]{{0, 89, 0}}) {
		
		private double stdParallel;
		
		public void initialize(double... params) {
			this.stdParallel = toRadians(params[0]);
			this.shape = Shape.rectangle(2*Math.PI, Math.PI/Math.cos(stdParallel));
		}
		
		public double[] project(double lat, double lon) {
			return new double[] {lon, lat/cos(stdParallel)};
		}
		
		public double[] inverse(double x, double y) {
			return new double[] {y*cos(stdParallel), x};
		}
	};
	
	
	public static final Projection GALL_ORTHOGRAPHIC = new Projection(
			"Gall-Peters", Shape.rectangle(2*Math.PI, 4), 0b1111, Type.CYLINDRICAL, Property.EQUAL_AREA, 0,
			"somewhat controversial", "with least distortion at 45\u00B0") {
		
		public double[] project(double lat, double lon) {
			return new double[] {lon, sin(lat)*shape.yMax};
		}
		
		public double[] inverse(double x, double y) {
			return new double[] { asin(y/shape.yMax), x};
		}
	};
	
	
	public static final Projection HOBO_DYER = new Projection(
			"Hobo-Dyer", Shape.rectangle(2*PI, 3.178), 0b1111, Type.CYLINDRICAL, Property.EQUAL_AREA, 2,
			null, "with least distortion at 37.5\u00B0") {
		
		public double[] project(double lat, double lon) {
			return new double[] {lon, sin(lat)*shape.yMax};
		}
		
		public double[] inverse(double x, double y) {
			return new double[] { asin(y/shape.yMax), x };
		}
	};
	
	
	public static final Projection BEHRMANN = new Projection(
			"Behrmann", Shape.rectangle(2*PI, 8/3.), 0b1111, Type.CYLINDRICAL, Property.EQUAL_AREA, 3,
			null, "with least distortion at 30\u00B0") {
		
		public double[] project(double lat, double lon) {
			return new double[] {lon, sin(lat)*shape.yMax};
		}
		
		public double[] inverse(double x, double y) {
			return new double[] { asin(y/shape.yMax), x };
		}
	};
	
	
	public static final Projection LAMBERT = new Projection(
			"Lambert cylindrical", Shape.rectangle(2*PI, 2), 0b1111, Type.CYLINDRICAL, Property.EQUAL_AREA, 2,
			null, "with least distortion along the equator") {
		
		public double[] project(double lat, double lon) {
			return new double[] {lon, sin(lat)*shape.yMax};
		}
		
		public double[] inverse(double x, double y) {
			return new double[] { asin(y*shape.yMax), x };
		}
	};
	
	
	public static final Projection EQUAL_AREA = new Projection(
			"Cylindrical Equal-area", "A generalized equal-area cylindrical projection.",
			null, 0b1111, Type.CYLINDRICAL, Property.EQUAL_AREA, 2,
			new String[]{"Std. parallel"}, new double[][]{{0, 89, 30}}) {
		
		public void initialize(double... params) {
			this.shape = Shape.rectangle(2*PI, 2/pow(cos(toRadians(params[0])), 2));
		}
		
		public double[] project(double lat, double lon) {
			return new double[] {lon, sin(lat)*shape.yMax};
		}
		
		public double[] inverse(double x, double y) {
			return new double[] { asin(y/shape.yMax), x };
		}
	};
	
	
	public static final Projection GALL_STEREOGRAPHIC = new Projection(
			"Gall Stereographic", Shape.rectangle(2*PI, 1.5*PI), 0b1111, Type.CYLINDRICAL,
			Property.COMPROMISE, 2) {
		
		public double[] project(double lat, double lon) {
			return new double[] {lon, tan(lat/2)*(1+sqrt(2))};
		}
		
		public double[] inverse(double x, double y) {
			return new double[] { 2*atan(y/(1+sqrt(2))), x };
		}
	};
	
	
	public static final Projection MILLER = new Projection(
			"Miller", Shape.rectangle(2*PI, 2.5*log(tan(9*PI/20))), 0b1111, Type.CYLINDRICAL,
			Property.COMPROMISE, 2) {
		
		public double[] project(double lat, double lon) {
			return new double[] {lon, log(tan(PI/4+.8*lat/2))/.8};
		}
		
		public double[] inverse(double x, double y) {
			return new double[] {atan(sinh(y*.8))/.8, x};
		}
	};
	
	
	public static final Projection CENTRAL = new Projection(
			"Central Cylindrical", Shape.rectangle(2*PI, 2*PI), 0b0111, Type.CYLINDRICAL,
			Property.PERSPECTIVE, 2) {
		
		public double[] project(double lat, double lon) {
			return new double[] {lon, tan(lat)};
		}
		
		public double[] inverse(double x, double y) {
			return new double[] {atan(y), x};
		}
	};
}
