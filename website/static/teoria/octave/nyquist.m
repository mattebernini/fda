pkg load control

s = tf('s');
G = input("G(s) = ");

hf = figure();
nyquist(G);
print(hf, "website/static/teoria/files/nyquist.jpg", "-djpg");
