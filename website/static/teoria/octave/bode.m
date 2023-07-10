pkg load control

s = tf('s');
G = input("G(s) = ");

hf = figure();
margin(G);
print(hf, "website/static/teoria/files/bode.jpg", "-djpg");
