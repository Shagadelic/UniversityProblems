#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;

class Spiel
{
private:
    string spieltag;
    string heimMannschaft;
    string auswaertsMannschaft;
    string heimTore;
    string auswaertsTore;
public:
    Spiel(string spieltagInit, string heimMannschaftInit, string auswaertsMannschaftInit, string heimToreInit, string auswaertsToreInit) {
        spieltag = spieltagInit;
        heimMannschaft = heimMannschaftInit;
        auswaertsMannschaft = auswaertsMannschaftInit;
        heimTore = heimToreInit;
        auswaertsTore = auswaertsToreInit;
    }
    //Zugriff auf private Variablen über public getter Funktionen
    string get_spieltag(){
        return spieltag;
    }
    string get_heimMannschaft(){
        return heimMannschaft;
    }
    string get_auswaertsMannschaft(){
        return auswaertsMannschaft;
    }
    string get_heimTore(){
        return heimTore;
    }
    string get_auswaertsTore(){
        return auswaertsTore;
    }
};

class Verein
{
    public:
    string name;
    int punkte;
    int tore;
    int gegentore;
    int tordiff;

    Verein(string nameInit, int punkteInit = 0, int toreInit = 0, int gegentoreInit = 0) {
        name = nameInit;
        punkte = punkteInit;
        tore = toreInit;
        gegentore = gegentoreInit;
    }
    //setzt die Tordifferenz
    void set_tordiff(){
        tordiff = tore-gegentore;
    }
};

int main(){


    /**************************************************************************************************************
    string path = "0";
    cout<<"Geben sie den Dateipfad von Bundesliga.csv ein (Bundesliga.csv wird ergänzt): ";
    cin>> path;
    ***************************************************************************************************************/


    //fstream Objekt
    fstream file;
    //Öffnet die Bundesliga.csv Tabelle im Lesemodus, Pfad der Datei muss unter Umständen angepasst/eingegeben werden.

    //Fester Pfad muss unter Umständen geändert werden.
    file.open("../Fußballtabelle/Bundesliga.csv", fstream::in);

    //**************************************************************************************************************
    //Bundesliga.csv wird an eingegebener Stelle gesucht.
    //file.open(path+"/Bundesliga.csv", fstream::in);
    //**************************************************************************************************************

    //Fehlermeldung + Ende, falls keine Datei geöffnet wurde
    if(!file){
        cerr<<"File not found"<<endl;
        exit(1);
    }
    //Spiel-liste
    vector <Spiel*> spielListe;
    //Veresins-liste
    vector <Verein*> vereinsListe;
    //Veriablen in die die Zeilen gespeichert werden.
    string tag = "";
    string team = "";
    string gegner = "";
    string tore ="" ;
    string austore ="" ;
    //Sorgt dafür, dass die erste Zeile nicht in der while Schleife eingelesen wird, indem sie jetzt einmal ausgelesen wird.
    string weg;
    getline(file,weg);
    //Solange das Ende des Files nicht erreicht wurde, wird ein neues Spiel Objekt angelegt worin die daten gespeichert werden.
    while (!file.eof()) {
        //Liest aus dem geöffneten file, speichert Daten in string Variablen, bis zur Abgrenzung durch ';' oder aber am Ende der Zeile durch '\n'.
        getline(file,tag,';');
        getline(file,team,';');
        getline(file,gegner,';');
        getline(file,tore,';');
        getline(file,austore,'\n');
        //Legt einen Pointer für ein Spielobjekt an.
        Spiel*tmp =new Spiel(tag, team, gegner, tore, austore);
        //Zeiger für das Spiel wird in einem Vector gespeichert
        spielListe.push_back(tmp);
    }
    //File wird geschlossen
    file.close();

    //neue Vereinsobjekte werden angelegt und in einem Vector gespeichert.
    for(unsigned int i = 0; i < spielListe.size(); i++){
        //Anfangs geht man davon aus, dass in der Vereinsliste keine der Manschaften drin ist.
        bool heimIn = false;
        bool auswaertsIn = false;
        for(unsigned int j = 0; j < vereinsListe.size(); j++){
            //Falls die Heimmanschaft des Spiels an spielListe[i] in der Vereinsliste vertreten ist, wird der heimIn Wert auf true gesetzt.
            if(spielListe[i]->get_heimMannschaft()==vereinsListe[j]->name){
                heimIn = true;
            }
            //Falls die Auswaertsmanschaft des Spiels an spielListe[i] in der Vereinsliste vertreten ist, wird der auswaertsIn Wert auf true gesetzt.
            if(spielListe[i]->get_auswaertsMannschaft()==vereinsListe[j]->name){
                auswaertsIn = true;
            }
        }
        //Falls heimIn false blieb wird die Heimmanschaft in die Vereinsliste aufgenommen.
        if(!heimIn){
            Verein* tmp = new Verein(spielListe[i]->get_heimMannschaft());
            vereinsListe.push_back(tmp);
        }
        //Falls auswaertsIn false blieb wird die Auswaertsmanschaft in die Vereinsliste aufgenommen.
        if(!auswaertsIn){
            Verein* tmp = new Verein(spielListe[i]->get_auswaertsMannschaft());
            vereinsListe.push_back(tmp);
        }
    }
    //Setzt Punkte der Vereine
    for(unsigned int i = 0; i < spielListe.size(); i++){
        string sieger = "";
        bool unentschieden = false;
        //findet raus wer der Sieger ist.
        spielListe[i]->get_heimTore() > spielListe[i]->get_auswaertsTore() ? sieger=spielListe[i]->get_heimMannschaft() : sieger=spielListe[i]->get_auswaertsMannschaft();
        //findet raus ob das Spiel ein Unentschieden war.
        spielListe[i]->get_heimTore() == spielListe[i]->get_auswaertsTore() ? unentschieden = true : unentschieden = false;

        //Geht die Vereinsliste durch und gibt allen beteiligten einen Punkt, wenn es das Spiel ein Unentschieden war.
        if(unentschieden){
            for(unsigned int j = 0; j < vereinsListe.size(); j++){
                if(vereinsListe[j]->name == spielListe[i]->get_heimMannschaft() || vereinsListe[j]->name == spielListe[i]->get_auswaertsMannschaft())
                    vereinsListe[j]->punkte+=1;
            }
        }
        //Geht die Vereinsliste durch und gibt dem Sieger 3 Punkte.
        else{
            for(unsigned int j = 0; j < vereinsListe.size(); j++){
                if(vereinsListe[j]->name == sieger){
                    vereinsListe[j]->punkte+=3;
                }
            }
        }
    }
    //Setzt Tore/Gegentore der Vereine
    //falls Heimmanschaft, werden die Tore um die Anzahl an Toren erhöht, die Gegentore um die Auswaertstoranzahl.
    //falls Auswaertsmannschaft, werden die Tore um die Anzahl an Auswaertstoren erhöht, die Gegentore um die Toranzahl.
    for(unsigned int i = 0; i < spielListe.size(); i++){
        for(unsigned int j = 0; j < vereinsListe.size(); j++){
            if(vereinsListe[j]->name == spielListe[i]->get_heimMannschaft()){
                vereinsListe[j]->tore += stoi(spielListe[i]->get_heimTore());
                vereinsListe[j]->gegentore += stoi(spielListe[i]->get_auswaertsTore());
            }
            else if(vereinsListe[j]->name == spielListe[i]->get_auswaertsMannschaft()){
                vereinsListe[j]->tore += stoi(spielListe[i]->get_auswaertsTore());
                vereinsListe[j]->gegentore += stoi(spielListe[i]->get_heimTore());
            }
        }
    }
    //Setzt Tordifferenz, nachdem Tore und Gegentore gesetzt wurden.
    for(unsigned int i = 0; i < vereinsListe.size(); i++){
        vereinsListe[i]->set_tordiff();
    }
    //Selectionsort
    //Läuft beim ersten lauf bis zum Ende dann jeweils einen Schritt weniger.
    int cd=0;
    for(unsigned int i = 1; i < vereinsListe.size(); i++){
        Verein* min=vereinsListe[0];
        int index = 0;
        int val;
        for(unsigned j = 1; j < vereinsListe.size()-cd; j++){
            if(vereinsListe[j]->punkte < min->punkte){
                min = vereinsListe[j];
                index= j;
            }
            else if(vereinsListe[j]->punkte == min->punkte && vereinsListe[j]->tordiff < min->tordiff){
                min = vereinsListe[j];
                index= j;
            }
            else if(vereinsListe[j]->punkte == min->punkte && vereinsListe[j]->tordiff == min->tordiff && vereinsListe[j]->tore < min->tore){
                min = vereinsListe[j];
                index= j;
            }
            val=j;
        }
        cd+=1;
        if((min->punkte < vereinsListe[val]->punkte) || (min->punkte == vereinsListe[val]->punkte && min->tordiff < vereinsListe[val]->tordiff) || (min->punkte == vereinsListe[val]->punkte && min->tordiff == vereinsListe[val]->tordiff && min->tore < vereinsListe[val]->tore)){
            Verein* tmp = vereinsListe[val];
            vereinsListe[val] = vereinsListe[index];
            vereinsListe[index] = tmp;

        }
    }


    /**************************************************************************************************************************
    path="0";
    cout<<"Geben sie den Pfad ein wo Fussballtabelle.csv gespeichert werden soll (/Fussballtabelle.csv wird ergänzt): "<<endl;
    cin>>path;
    ***************************************************************************************************************************/


    //Öffnet "Fussballtabelle.csv" genanntes file mit schreibzugriff.


    //*************************************************************************************************************************
    //Speichert die Datei im angegebenen Verzeichnis.
    //file.open(path+"/Fussballtabelle.csv",fstream::out);
    //*************************************************************************************************************************

    //Speichert die Datei im Build Ordner.
    file.open("Fussballtabelle.csv",fstream::out);
    //Headerzeile
    file <<"Platz"<<";"<<"Mannschaft"<<";"<<"Punkte"";"<<"Tore"";"<<"Gegentore"";"<<"Tordifferenz"<<"\n";
    //Schreibt inhalte der Vereinstabelle ins file rein.
    for(unsigned int i = 0; i < vereinsListe.size(); i++){
        file <<i+1<<";"<<vereinsListe[i]->name<<";"<<vereinsListe[i]->punkte<<";"<<vereinsListe[i]->tore<<";"<<vereinsListe[i]->gegentore<<";"<<vereinsListe[i]->tordiff<<"\n";
    }
    //schließt den Buffer.
    file.close();

    /*
    //Gibt die geordnete Vereinstabelle Tabelle aus.
    for(unsigned int i=0;i<vereinsListe.size();i++){
        cout<<vereinsListe[i]->name<<"  "<<vereinsListe[i]->punkte<<"  "<<vereinsListe[i]->tore<<"  "<<vereinsListe[i]->gegentore<<"  "<<vereinsListe[i]->tordiff<<endl;
    }
    */
}
