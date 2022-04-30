public class Display {
    private int heim = 0;
    private int gast = 0;

    public Display(){

    }
    public void setHeim(int punkte){
        this.heim = punkte;
    }

    public void setGast(int punkte){
        this.gast = punkte;
    }

    public int getHeim(){
        return this.heim;
    }

    public int getGast(){
        return this.gast;
    }
}
