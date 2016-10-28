
public class Pixel {
	
	private int red;
	private int green;
	private int blue;
	
	/**Metodo Constructor del Pixel */
	public Pixel (int r, int g, int b) {
		
		red = r;
		green = g;
		blue = b;
		
		if (r>255)
			r=255;
		if (r<0)
			r=0;
		if (g>255)
			g=255;
		if (g<0)
			g=0;
		if (b>255)
			b=255;
		if (b<0)
			b=0;		
	}
	/**Metodo Constructor de un Pixel con los atributos de otro pixel
	 */
	public Pixel (Pixel px){
		
		red = px.getRed();
		green = px.getGreen();
		blue = px.getBlue();
	
	}
	/**Metodo que devuelve el valor de red de un pixel mediante un entero
	 */
	public int getRed (){
		return red;
	}
	
	/**Metodo que devuelve el valor de green de un pixel mediante un entero
	 */
	public int getGreen (){
		return green;
	}
	
	/**Metodo que devuelve el valor de blue de un pixel mediante un entero
	 */
	public int getBlue (){
		return blue;
	}
	
	/**Metodo que devuelve un String que contiene el valor del red, green y blue de un pixel
	 */
	public String toString (){
		String pixtext;
		
		pixtext=("Red: " + red +" Green: " + green +" Blue :" + blue);
		return pixtext;
	}
}

	
