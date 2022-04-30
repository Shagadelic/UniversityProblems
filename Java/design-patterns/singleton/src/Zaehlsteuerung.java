import java.util.ArrayList;

public class Zaehlsteuerung {

    private static Zaehlsteuerung singleInstance ;
    private ArrayList<Display> displays;
    private int heimPkt = 0;
    private int gastPkt = 0;

    private Zaehlsteuerung( ) {
        this.displays = new ArrayList<>();
    }

    public void erhoeheHeim(){
        this.heimPkt++;
        updateDisplays();
    }
    public void erhoeheGast(){
        this.gastPkt++;
        updateDisplays();
    }

    public void reset(){
        this.heimPkt=0;
        this.gastPkt=0;
        updateDisplays();
    }

    public void updateDisplays(){
        for(Display disp : displays){
            disp.setGast(this.gastPkt);
            disp.setHeim(this.heimPkt);
        }
    }

    public void displayInfo(){
        for(Display disp : displays){
            System.out.println(disp.getHeim());
            System.out.println(disp.getGast());
        }
    }

    public void addDisplay(Display disp){
        this.displays.add(disp);
    }

    public static synchronized Zaehlsteuerung getInstanz () {
        if ( singleInstance == null ) {
            singleInstance = new Zaehlsteuerung( ) ;
        }
        return singleInstance ;
    }

    public static void main (String[]args){
        //Adds one display and two controls (Singleton) to the GUI
        Display disp1 = new Display();
        Zaehlsteuerung zaehl1 = Zaehlsteuerung.getInstanz();
        Zaehlsteuerung zaehl2 = Zaehlsteuerung.getInstanz();
        zaehl1.addDisplay(disp1);
        zaehl2.addDisplay(disp1);
        System.out.println(zaehl1.equals(zaehl2));
        GUI frame = new GUI(zaehl1, zaehl2, disp1);

    }
}
