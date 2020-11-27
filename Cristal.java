package cristales;

import org.opencv.core.Core;
import org.opencv.core.Mat;
import static org.opencv.imgcodecs.Imgcodecs.imread;
import org.opencv.imgproc.Imgproc;
import static cristales.funciones.imshow;
import java.util.ArrayList;
import java.util.List;
import org.opencv.core.CvType;
import org.opencv.core.MatOfPoint;
import org.opencv.core.MatOfPoint2f;
import org.opencv.core.Point;
import org.opencv.core.RotatedRect;
import org.opencv.core.Scalar;

public class Cristales {
    public static void main(String[] args) {
        
        System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
     
        Mat im = imread("resources\\4.jpeg");
        Mat imColor = new Mat();
        Mat imBw = new Mat();
        Mat imClose = new Mat();
        Mat mask = Mat.ones(10,10, CvType.CV_32F);
        
        double maxVal = 0;
        int maxValId = 0;
        
        double ang;
        Mat points = new Mat();
        double x1 = 0;
        double y1 = 0;
        double x2 = 0;
        double y2 = 0;
        
        Imgproc.cvtColor(im,imColor,Imgproc.COLOR_BGR2GRAY);
        Imgproc.threshold(imColor, imBw, 100, 255, Imgproc.THRESH_BINARY_INV);
        Imgproc.morphologyEx(imBw, imClose, Imgproc.MORPH_CLOSE, mask);
        
        List<MatOfPoint> contornos = new ArrayList<>();
        Imgproc.findContours(imClose, contornos, new Mat(), Imgproc.RETR_EXTERNAL, Imgproc.CHAIN_APPROX_SIMPLE);
        for(int i=0;i<contornos.size();i++){
            double area = Imgproc.contourArea(contornos.get(i));
            if (maxVal < area) {
                maxVal = area;
                maxValId = i;
            }
        } 
        
        Imgproc.drawContours(im, contornos, maxValId, new Scalar(0, 255, 0),10);     
        RotatedRect bounding = Imgproc.minAreaRect(new MatOfPoint2f(contornos.get(maxValId).toArray()));
        Imgproc.boxPoints(bounding, points);
        
        if(bounding.size.width < bounding.size.height){
            ang = 90-bounding.angle;
            x1 = points.get(3,0)[0]+(points.get(0,0)[0] - points.get(3,0)[0])/2 ;
            y1 = points.get(0,1)[0]+(points.get(3,1)[0] - points.get(0,1)[0])/2 ;
            x2 = points.get(2,0)[0]+(points.get(1,0)[0] - points.get(2,0)[0])/2 ;
            y2 = points.get(1,1)[0]+(points.get(2,1)[0] - points.get(1,1)[0])/2 ;
        
        }else{
            ang = -bounding.angle;
            x1 = points.get(3,0)[0]+(points.get(2,0)[0] - points.get(3,0)[0])/2 ;
            y1 = points.get(2,1)[0]+(points.get(3,1)[0] - points.get(2,1)[0])/2 ;
            x2 = points.get(0,0)[0]+(points.get(1,0)[0] - points.get(0,0)[0])/2 ;
            y2 = points.get(1,1)[0]+(points.get(0,1)[0] - points.get(1,1)[0])/2 ;
        }
        
        Imgproc.line(im, new Point(x1,y1), new Point(x2,y2), new Scalar(255, 0, 0), 10);
        Imgproc.line(im, new Point(0,im.height()/2), new Point(im.width(),im.height()/2), new Scalar(0, 0, 255), 10);
        
        System.out.println(ang);
        imshow(im); 
    }
}
