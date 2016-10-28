
public class Prueba {

	public static void main(String[] args) {

		int brillo=0;

		BitmapUtils img = new BitmapUtils();
		
		Bitmap bmp = img.read("/home/dviterig/Downloads/color_pic/imagen.jpg");
		Bitmap n = new Bitmap (bmp.getWidth(),bmp.getHeight());
		for(int x = 0; x<bmp.getWidth(); x++){
			for(int y = 0; y<bmp.getHeight(); y++){
				n.setPixel(x,y,bmp.getPixel(x,y));
			}
		}

		brillo = n.brightness();

		System.out.printf("%d %n", brillo);

		if(brillo < 60){
			for(int x = 0; x<bmp.getWidth(); x++){
				for(int y = 0; y<bmp.getHeight(); y++){
					n.bright_up(x,y);
				}
			}
		}

		img.save("/home/dviterig/Downloads/color_pic/resultado.jpg",n);
		
		
	}
}