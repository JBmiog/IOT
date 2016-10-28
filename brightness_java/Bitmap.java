
public class Bitmap {
	
	private Pixel matriz [][];
	private Pixel aux [][];
	
	private int ancho;
	private int largo;

	private int brightness;
	private int counter;
	
	/**Metodo Constructor del Bitmap */
	public Bitmap (int width, int height){
		int x;
		int y;
		matriz = new Pixel[width][height];
		
		ancho=width;
		largo=height;
		
		for(x=0; x<width; x++){
			for(y=0; y<height; y++){
				matriz[x][y] = new Pixel(255,255,255);
			}	
		}
	}
	
	/**Metodo Constructor de la copia de otro Bitmap*/
	public Bitmap (Bitmap o){
		int x;
		int y;
		ancho=o.getWidth();
		largo=o.getHeight();
		
		
		matriz = new Pixel[ancho][largo];
		
		for(x=0; x<ancho; x++){
			for(y=0; y<largo; y++){
				matriz[x][y] = new Pixel(o.getPixel(x,y));
			}
		}
	}
	/**Metodo de tipo Pixel[][], que devuelve un Bitmap copia de otro Bitmap */
	public Pixel[][] getBitmap(){
		int x;
		int y;
		
		aux = new Pixel [ancho][largo];
		
		for(x=0; x<ancho; x++){
			for(y=0; y<largo; y++){
				aux[x][y] = new Pixel(getPixel(x,y));
			}
		}
		
		return aux;
	}
	
	/**Metodo de tipo Pixel, que devuelve un Pixel localizado en una posicion de una matriz de Pixeles  */
	public Pixel getPixel(int x, int y){
		
		return matriz[x][y];
	}
	
	/**Metodo de tipo entero, que devuelve el largo de la matriz de un Bitmap */
	public int getHeight (){
		return largo;
	}
	
	/**Metodo de tipo entero, que devuelve el ancho de la matriz de un Bitmap */
	public int getWidth(){
		return ancho;
	}
	
	/**Metodo que establece un Pixel de una matriz de Pixeles en la posicion (x,y) como copia del Pixel p */
	public void setPixel (int x, int y, Pixel p){
		matriz[x][y] = p;
	}
	
	/**Metodo que devuelve un String con la representacion del Bitmap */
	public String toString(){
		String representacion=null;
		int x;
		int y;
		
		
		for (x=0; x<ancho; x++){
			for (y=0; y<largo; y++){
				representacion = representacion + matriz[x][y].toString();
			}
			
		}
		return representacion;
	}

	public int brightness(){
		int x;
		int y;
		int b=0;
		counter=0;

		for(x=0; x<ancho; x=x+50){
			for(y=0; y<largo; y=y+50){
				b += matriz[x][y].getRed()*(2126)/(10000) + matriz[x][y].getGreen()*(7152)/(10000) + matriz[x][y].getBlue()*(722)/(10000);
				counter++;
			}
		}
		brightness = b/counter;
		return brightness;
	}

	public void bright_up(int x, int y){
		double new_r = matriz[x][y].getRed()*(60-brightness)/(15);
		double new_g = matriz[x][y].getGreen()*(60-brightness)/(15);
		double new_b = matriz[x][y].getBlue()*(60-brightness)/(15);

		if (new_r > 255)
			new_r = 255;

		if (new_g > 255)
			new_g = 255;

		if (new_b > 255)
			new_b = 255;

		Pixel aux = new Pixel ((int)new_r,(int)new_g,(int)new_b);
		matriz[x][y]=aux;
	}
}
