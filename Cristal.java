package cristales;

import org.opencv.core.Core;
import org.opencv.core.Mat;
import static org.opencv.imgcodecs.Imgcodecs.imread;
import org.opencv.imgproc.Imgproc;
import static cristales.funciones.imshow;
import java.awt.FlowLayout;
import java.awt.Image;
import java.awt.image.BufferedImage;
import java.awt.image.DataBufferByte;
import java.util.ArrayList;
import java.util.List;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;
import org.opencv.core.CvType;
import org.opencv.core.MatOfPoint;
import org.opencv.core.MatOfPoint2f;
import org.opencv.core.Point;
import org.opencv.core.RotatedRect;
import org.opencv.core.Scalar;
import org.opencv.videoio.VideoCapture;

public class Cristales {
    public static void main(String[] args) throws InterruptedException {
        
        System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
        
        JFrame jframe=new JFrame();
        JLabel lbl=new JLabel();
        jframe.setLayout(new FlowLayout());
        jframe.setSize(700,700);
        jframe.add(lbl);
        jframe.setVisible(true);
        jframe.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
       
        VideoCapture camara = new VideoCapture(1);
        Thread.sleep(1000);
        Mat frame = new Mat();
        while (true){
            camara.read(frame);
            //Mat im = imread("resources\\6.jpeg");
            Mat imColor = new Mat();
            Mat imBw = new Mat();
            Mat imClose = new Mat();
            Mat mask = Mat.ones(10,10, CvType.CV_32F);

            double maxVal = 0;
            int maxValId = 0;

            double ang;
            Mat points = new Mat();
            double x1;
            double y1;
            double x2;
            double y2;

            Imgproc.cvtColor(frame,imColor,Imgproc.COLOR_BGR2GRAY);
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

            Imgproc.drawContours(frame, contornos, maxValId, new Scalar(0, 255, 0),10);     
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

            Imgproc.line(frame, new Point(x1,y1), new Point(x2,y2), new Scalar(255, 0, 0), 10);
            Imgproc.line(frame, new Point(0,frame.height()/2), new Point(frame.width(),frame.height()/2), new Scalar(0, 0, 255), 10);
            System.out.println("Angulo detectado:" + ang);
            //imshow(im); 
            //imshow(imBw);
            
            Image im = Mat2BufferedImage(frame);
            ImageIcon icon = new ImageIcon(im);
            lbl.setIcon(icon);
        }
    }
    
    public static BufferedImage Mat2BufferedImage(Mat m){
        int type = BufferedImage.TYPE_BYTE_GRAY;
        if ( m.channels() > 1 ) {
            type = BufferedImage.TYPE_3BYTE_BGR;
        }
        int bufferSize = m.channels()*m.cols()*m.rows();
        byte [] b = new byte[bufferSize];
        m.get(0,0,b); // get all the pixels
        BufferedImage image = new BufferedImage(m.cols(),m.rows(), type);
        final byte[] targetPixels = ((DataBufferByte) image.getRaster().getDataBuffer()).getData();
        System.arraycopy(b, 0, targetPixels, 0, b.length);  
        return image;
    }
}
