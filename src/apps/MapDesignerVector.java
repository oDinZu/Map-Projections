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
package apps;
import java.io.File;
import java.io.IOException;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;
import java.util.function.DoubleConsumer;

import javax.xml.parsers.ParserConfigurationException;

import org.xml.sax.SAXException;

import dialogs.ProgressBarDialog;
import javafx.application.Platform;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Node;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.control.Button;
import javafx.scene.control.Separator;
import javafx.scene.layout.HBox;
import javafx.scene.layout.StackPane;
import javafx.scene.layout.VBox;
import javafx.stage.FileChooser;
import javafx.stage.Stage;
import maps.Azimuthal;
import maps.Conic;
import maps.Cylindrical;
import maps.Misc;
import maps.MyProjections;
import maps.Projection;
import maps.Pseudocylindrical;
import maps.Robinson;
import maps.Tetrahedral;
import maps.Tobler;
import maps.WinkelTripel;
import utils.Procedure;
import utils.SVGMap;
import utils.SVGMap.Command;
import utils.SVGMap.Path;

/**
 * An application to make vector oblique aspects of map projections
 * 
 * @author Justin Kunimune
 */
public class MapDesignerVector extends MapApplication {

	public static final void main(String[] args) {
		launch(args);
	}
	
	
	
	private static final FileChooser.ExtensionFilter[] VECTOR_TYPES = {
			new FileChooser.ExtensionFilter("SVG", "*.svg") };
	
	private static final Projection[] PROJ_ARR = { Cylindrical.MERCATOR,
			Cylindrical.EQUIRECTANGULAR, Cylindrical.EQUAL_AREA, Cylindrical.GALL,
			Azimuthal.STEREOGRAPHIC, Azimuthal.POLAR, Azimuthal.EQUAL_AREA, Azimuthal.GNOMONIC,
			Azimuthal.PERSPECTIVE, Conic.LAMBERT, Conic.EQUIDISTANT, Conic.ALBERS, Tetrahedral.LEE,
			Tetrahedral.TETRAGRAPH, Pseudocylindrical.SINUSOIDAL, Pseudocylindrical.MOLLWEIDE,
			Tobler.TOBLER, Misc.AITOFF, Misc.VAN_DER_GRINTEN, Robinson.ROBINSON,
			WinkelTripel.WINKEL_TRIPEL, Misc.PEIRCE_QUINCUNCIAL, Misc.GUYOU,
			Misc.TWO_POINT_EQUIDISTANT, Misc.HAMMER_RETROAZIMUTHAL, Pseudocylindrical.LEMONS,
			MyProjections.EXPERIMENT, MyProjections.PSEUDOSTEREOGRAPHIC,
			MyProjections.HYPERELLIPOWER, Tetrahedral.TETRAPOWER, Tetrahedral.TETRAFILLET,
			MyProjections.TWO_POINT_EQUALIZED };
	
	private static final int DEF_MAX_VTX = 5000;
	private static final int FAST_MAX_VTX = 2000;
	
	
	private Node aspectSelector;
	private Button saveBtn;
	private double[] aspect;
	private SVGMap input;
	private Canvas viewer;
	
	
	
	public MapDesignerVector() {
		super("Map Designer");
	}
	
	
	
	@Override
	public void start(Stage root) {
		super.start(root);
		new Thread(() -> {
			setInput(new File("input/Basic.svg")); //this automatically updates the map//TODO: this should cause the buttons to grey out
		}).start();
	}
	
	
	@Override
	protected Node makeWidgets() {
		this.aspect = new double[3];
		final Node inputSelector = buildInputSelector(VECTOR_TYPES,
				VECTOR_TYPES[0], this::setInput);
		final Node projectionSelector = buildProjectionSelector(PROJ_ARR,
				Procedure.concat(this::updateMap, this::hideAspect));
		this.aspectSelector = buildAspectSelector(this.aspect, this::updateMap);
		final Node parameterSelector = buildParameterSelector(this::updateMap);
		this.saveBtn = buildSaveButton(true, "map", VECTOR_TYPES,
				VECTOR_TYPES[0], ()->true, this::calculateAndSaveMap);
		aspectSelector.managedProperty().bind(aspectSelector.visibleProperty());
		
		final VBox layout = new VBox(5,
				inputSelector, new Separator(), projectionSelector,
				new Separator(), aspectSelector, parameterSelector,
				new Separator(), saveBtn);
		
		layout.setAlignment(Pos.CENTER);
		layout.setPrefWidth(GUI_WIDTH);
		
		viewer = new Canvas(IMG_WIDTH, IMG_WIDTH);
		
		final HBox gui = new HBox(10, layout, viewer);
		gui.setAlignment(Pos.CENTER);
		StackPane.setMargin(gui, new Insets(10));
		
		return gui;
	}
	
	
	private void setInput(File file) {
		saveBtn.setDisable(true);
		
		try {
			input = new SVGMap(file);
		} catch (IOException e) {
			showError("File not found!",
					"We couldn't find "+file.getAbsolutePath()+".");
		} catch (SAXException e) {
			showError("Unreadable file!",
					"We couldn't read "+file.getAbsolutePath()+". It may be corrupt or an unreadable format.");
		} catch (ParserConfigurationException e) {
			// TODO: Handle this
			e.printStackTrace();
		} finally {
			saveBtn.setDisable(false);
		}
		
		updateMap();
	}
	
	
	
	private void hideAspect() {
		aspectSelector.setVisible(this.getProjection().hasAspect());
	}
	
	
	private void updateMap() {
		loadParameters();
		int maxVtx = this.getParamsChanging() ? FAST_MAX_VTX : DEF_MAX_VTX;
		final Iterable<Path> transformed = map(input, input.size()/maxVtx+1, aspect.clone(), null);
		drawImage(transformed, viewer);
	}
	
	
	private void calculateAndSaveMap(File file, ProgressBarDialog pBar) {
		loadParameters();
		final Iterable<Path> transformed = map(input, 1, aspect.clone(), pBar::setProgress); //calculate
		try {
			input.save(transformed, file, pBar::setProgress); //save
		} catch (IOException e) {
			showError("Failure!",
					"Could not access "+file.getAbsolutePath()+". It's possible that another program has it open.");
		}
	}
	
	
	public Iterable<Path> map(SVGMap input, int step, double[] pole, DoubleConsumer tracker) {
		List<Path> output = new LinkedList<Path>();
		int i = 0;
		for (Path path0: input) {
			if (path0.length() < step*3) 	continue;
			
			Path path1 = new Path();
			int counter = 0;
			for (Command cmd0: path0) {
				counter --;
				if (counter > 0 && cmd0.type != 'M' && cmd0.type != 'Z') 	continue;
				counter = step;
				
				Command cmd1 = new Command(cmd0.type, new double[cmd0.args.length]);
				for (int k = 0; k < cmd0.args.length; k += 2) {
					System.arraycopy(
							this.getProjection().project(cmd0.args[k+1], cmd0.args[k], pole), 0,
							cmd1.args, k, 2);
				}
				path1.add(cmd1);
			}
			output.add(path1);
			
			if (tracker != null) {
				i ++;
				tracker.accept((double)i/input.numCurves());
			}
		}
		return output;
	}
	
	
	private void drawImage(Iterable<Path> paths, Canvas c) {
		GraphicsContext g = c.getGraphicsContext2D();
		g.clearRect(0, 0, c.getWidth(), c.getHeight());
		g.beginPath();
		for (Path path: paths) {
			g.appendSVGPath(path.toString(0, 0, IMG_WIDTH, IMG_WIDTH));
		}
		g.stroke();
	}

}
