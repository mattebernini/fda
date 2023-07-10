pkg load control

s = tf('s');
G = input("G(s) = ");

hf = figure();
rlocus(G);
print(hf, "website/static/teoria/files/rlocus.jpg", "-djpg");
