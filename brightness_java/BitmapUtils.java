/*
 * 
 * Auxiliars methods for load/save bitmaps.
 */
import java.io.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.awt.*;
import java.awt.image.*;

import javax.imageio.ImageIO;
import javax.swing.*;


public class BitmapUtils {

    private BufferedImage bufferedImage;
    private WritableRaster raster;

    /**
     * Obtiene un bitmap 
     */ 
    private BitmapUtils(BitmapUtils other) {
        bufferedImage = 
            new BufferedImage(other.raster.getWidth(),
                              other.raster.getHeight(),
                              BufferedImage.TYPE_INT_RGB);

        raster = bufferedImage.getRaster();
        raster.setRect(other.bufferedImage.getRaster());
    }

    public BitmapUtils() {
       
    }
   /**
     * Obtiene un bitmap de un fichero
     * @param filename Fichero con la imagen 
     */ 

    public Bitmap read (String filename) {
    	  ImageIcon icon;

          try {
              if ((new File(filename)).exists())
                  icon = new ImageIcon(filename);
              else {
                  java.net.URL u = new java.net.URL(filename);
                  icon = new ImageIcon(u);
              }
          } catch (Exception e) { throw new RuntimeException(e); }
        
          Image image = icon.getImage();
          bufferedImage = 
              new BufferedImage(image.getWidth(null),
                                image.getHeight(null),
                                BufferedImage.TYPE_INT_RGB);
          Graphics g = bufferedImage.getGraphics();
          g.drawImage(image, 0, 0, null);
          g.dispose();

          raster = bufferedImage.getRaster();
    	  return getBitmap();
    }
     /**
     * Salva una imagen en un fichero
     * @param filename Fichero 
     * @param bmp Imagen
     */ 
    
    public void save (String filename, Bitmap bmp) {
    	setBitmap(bmp);
    	save(filename);
    }
    
   
    private void setBitmap(Bitmap bmp) {
        int w = bmp.getWidth();
        int h = bmp.getHeight();
       

        bufferedImage = new BufferedImage(w, h, BufferedImage.TYPE_INT_RGB);
        raster = bufferedImage.getRaster();

        for (int x = 0; x < w; x++) {
            for (int y = 0; y < h; y++) {
            	Pixel p = bmp.getPixel(x,y);
                raster.setPixel(x, y, new int[] {p.getRed(),p.getGreen(),p.getBlue()});
            }
        }
    }

    
    private Bitmap getBitmap() {
        int w = raster.getWidth() ;
        int h = raster.getHeight();

        Bitmap bmp = new Bitmap(w,h);

        for (int x = 0; x < w; x++) {
            for (int y = 0; y < h; y++) {
            	int [] p  = raster.getPixel(x, y, (int[]) null);
                bmp.setPixel(x,y, new Pixel(p[0],p[1],p[2]));
            }
        }

        return bmp;
    }
   
   
    public static ImageIcon toImageIcon( Bitmap bmp) {
        BitmapUtils copy = new BitmapUtils();
        copy.setBitmap(bmp);
        return new ImageIcon(copy.bufferedImage);
    }
   
       
    private static Pattern suffix = Pattern.compile(".*\\.(\\w{3,4})");
    
    private void save(String filename) {
        String type = "png";

        // detect the file type
        Matcher m = suffix.matcher(filename);
        if (m.matches()) {
            type = m.group(1);
        }

        try {
            ImageIO.write(bufferedImage, type, new File(filename)); 
        } catch(IOException e) { 
            throw new RuntimeException(e); 
        }
    }
    
}
