import processing.net.*;
Client myClient;

void setup(){
    size(200, 200);

    myClient = new Client(this, "127.0.0.1", 50007);
}

void draw(){
    //myClient.write("Paging Python!");
    String a = myClient.readString();
    println(a);

}
