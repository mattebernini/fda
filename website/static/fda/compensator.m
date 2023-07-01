pkg load control

% INPUT
fid = fopen('website/static/fda/in_fdt.txt', 'r');
lines = textscan(fid, '%s', 'Delimiter', '\n');
fclose(fid);

s = tf('s');
G = eval(lines{1}{1});  % Transfer function G(s)
R = eval(lines{1}{2});  % Transfer function R(s)
% Calculate compensated system S(s)
F = G * R;


% salvo bode plot
hf = figure();
margin(G);
title('Bode Plot of G');
print(hf, "website/static/fda/bode_plot.jpg", "-djpg");

hf = figure();
margin(F);
title('Bode Plot of compensate G');
print(hf, "website/static/fda/bode_plot_compensate.jpg", "-djpg");

% luogo delle radici
try
    [rldata, k_critico] = rlocus(G);
    hf = figure();
    rlocus(G);
    title('Root Locus of G');
    print(hf, "website/static/fda/rlocus_plot.jpg", "-djpg");
catch
    hf = figure();
    print(hf, "website/static/fda/rlocus_plot.jpg", "-djpg");
end
try
    [rldata, k_critico] = rlocus(F);
    hf = figure();
    rlocus(F);
    title('Root Locus of compensate G');
    print(hf, "website/static/fda/rlocus_plot_compensate.jpg", "-djpg");
catch
    hf = figure();
    print(hf, "website/static/fda/rlocus_plot_compensate.jpg", "-djpg");
end

% Calculate and plot the step response
hf = figure();
step(G);
title('Step Response of G');
xlabel('Time');
ylabel('Amplitude');
print(hf, "website/static/fda/step_response.jpg", "-djpg");

hf = figure();
step(F);
title('Step Response of compensate G');
xlabel('Time');
ylabel('Amplitude');
print(hf, "website/static/fda/step_response_compensate.jpg", "-djpg");

fid = fopen("website/static/fda/result.txt", "w");

% poli e zeri
[poli, zeri] = pzmap(F);


fdisp(fid, "poli");
fdisp(fid, poli);
fdisp(fid, "zeri");
fdisp(fid, zeri);
fdisp(fid, "k_critico");
[rldata, k_critico] = rlocus(F);
fdisp(fid, k_critico);
[modulo, fase, w_modulo, w_fase] = margin(F);  
fdisp(fid, "margine_di_modulo");
fdisp(fid, modulo);
fdisp(fid, "margine_di_fase");
fdisp(fid, fase);

% Bandwidth from Bode (-3 dB)
[mag, phase, wout] = bode(G);
db_threshold = -3;
mag_db = 20 * log10(squeeze(mag));
bw_indices = find(mag_db <= db_threshold);
bw_frequency = wout(bw_indices(1));
fdisp(fid, "bandwidth");
fdisp(fid, bw_frequency);

% 2nd order system
[num, den] = tfdata(G, 'v');
if length(den) ~= 3
    fdisp(fid, "The system is not second-order.");
    exit;
end

a1 = den(1);
a2 = den(2);
a3 = den(3);

natural_frequency = sqrt(1/(a1/a3));
damping_ratio = a2 * natural_frequency / (2 * a3);

rise_time = 1.8 / natural_frequency;
S = 100 * e^((-damping_ratio*pi)/sqrt(1-damping_ratio^2));
t_max = pi/(natural_frequency*sqrt(1-damping_ratio^2));
t_s = -log(0.05)/(damping_ratio * natural_frequency);
T_p = (2*pi)/(natural_frequency*sqrt(1-damping_ratio^2));

fdisp(fid, "Damping Ratio: (2nd order sys) " );
fdisp(fid, damping_ratio);
fdisp(fid, "Natural Frequency: (2nd order sys) " );
fdisp(fid, natural_frequency);
fdisp(fid, "Rise time to 90%: (2nd order sys) " );
fdisp(fid, rise_time);
fdisp(fid, "Max overshoot(%): (2nd order sys) " );
fdisp(fid, S);
fdisp(fid, "time to max overshoot: (2nd order sys) " );
fdisp(fid, t_max);
fdisp(fid, "settling time to 5%: (2nd order sys) " );
fdisp(fid, t_s);
fdisp(fid, "Oscillation period: (2nd order sys) " );
fdisp(fid, T_p);


fclose(fid);
exit