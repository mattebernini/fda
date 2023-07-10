pkg load control

s = tf('s');
G = input("G(s) = ");

hf = figure();
step(G);
print(hf, "website/static/teoria/files/step.jpg", "-djpg");
