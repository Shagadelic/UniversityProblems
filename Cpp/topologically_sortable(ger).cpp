/*
Takes in the number of dwarfes followed by their name.
Then takes the number of relations between them followed by those as the input.

5
Brokkr
Fafnir
Ottur
Regin
Sindri
5
Ottur < Sindri
Brokkr < Ottur
Regin < Ottur
Regin < Fafnir
Fafnir < Sindri

Output: possible

5
Brokkr
Fafnir
Ottur
Regin
Sindri
7
Fafnir < Regin
Ottur < Sindri
Brokkr < Regin
Fafnir < Sindri
Sindri < Brokkr
Brokkr < Fafnir
Regin < Ottur

Output: impossible
*/

#include <iostream>
#include <vector>
//Dictionary
#include <map>
using namespace std;

//Zwerg Objekt: hat einen Namen und eine Liste mit bekannten größeren Zwergen
struct Zwerg{
    //Der Name vom Zwerg
    string name;
    //markiert status (0: unbesucht, 1: besucht und im Suchvorgang, 2: besucht und fertig)
    int markierung=0;
    //Vector mit "bekannten" größeren Zwergen
    vector<Zwerg*> zwergLi;
    Zwerg(string n) {
        name=n;
    }
};
//Funktion die mithilfe einer Tiefensuche überprüft ob im Graph ein Kreis vorkommt (nur topologisch sortierbar wenn ungerichtet azyklisch)
void kreis(Zwerg* &z, string &moeglich){
    //wenn der Zwerg und seine größeren besucht wurden, dann gibt es nichts zu tun
    if(z->markierung==2){
        return;
    }
    //falls ein Zwerg während der Durchsuchung seiner größeren Zwerge gefunden wurde, dann gibt es einen Zyklus
    if(z->markierung==1){
        moeglich="impossible";
        return;
    }
    //Zwerg wird auf besucht gesetzt, wenn noch nicht besucht
    if(z->markierung==0){
        z->markierung=1;
    }
    //Suche geht in der Zwergenliste von z weiter
    for(auto grZ:z->zwergLi){
        kreis(grZ, moeglich);
    }
    //alle größeren wurden durchsucht, z ist fertig
    z->markierung=2;
}
//Liest die Eingaben ein
void run(map<string, Zwerg*> &aL){
        int n;
        cin>>n;
        //erstellt eine map Liste mit n Zwerg Objekten      
        string zwerg;
        for(int i=0;i<n;i++){
            //getline(cin,zwerg);
            cin>>zwerg;
            aL[zwerg]=new Zwerg(zwerg);
        }
        cin>>n;
        //fügt der ZwegenListe voḿ kleineren Zwerg den größeren Zwerg hinzu     
        string line;
        for(int i = 0; i<n;i++){
            string kleinererZwerg;
            string kleinerZeichen;
            string groessererZwerg;
            //Speichert Eingabe in Variablen (jeweils bis zum Leerzeichen)
            cin>>kleinererZwerg>>kleinerZeichen>>groessererZwerg;
            aL[kleinererZwerg]->zwergLi.push_back(aL[groessererZwerg]);
        }   
    }
int main(){
    //Dictionary mit String als key (Name vom Zwerg) und einem Zwerg* als value
    map<string, Zwerg*> zwergListe;
    //Variable die nach dem Durchsuchen ausgegeben wird, wird innerhalb von kreis() verändert wenn nötig
    string moeglich="possible";
    //Eingabe
    run(zwergListe);
	//Kreissuche mit jedem Zwerg als Startpunkt
    for(auto m:zwergListe){
        kreis(m.second,moeglich);
        if(moeglich=="impossible"){
            break;
        }
    }
    cout<<moeglich<<endl;
}