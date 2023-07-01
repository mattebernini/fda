pkg load control

% INPUT
fid = fopen('website/static/fda/in_matrici.txt', 'r');
combined_matrix = textscan(fid, '%s', 'Delimiter', '');
fclose(fid);

A = str2num(combined_matrix{1}{1});
B = str2num(combined_matrix{1}{2});
C = str2num(combined_matrix{1}{3});
D = str2num(combined_matrix{1}{4});

fid = fopen("website/static/fda/result.txt", "w");

% RISTAMPA INPUT
fdisp(fid, "** A");
fdisp(fid, A);
fdisp(fid, "** B");
fdisp(fid, B);
fdisp(fid, "** C");
fdisp(fid, C);
fdisp(fid, "** D");
fdisp(fid, D);


% analisi modale
fdisp(fid, "** Analisi Modale");
fdisp(fid, "-- Dato un autovalore landa = a + i*b --> modo = exp(a*t)*cos(b*t)");
% -----------------------------------------------------
[eigenvectors, eigenvalues] = eig(A);
eigenvalues = diag(eigenvalues);
for i = 1:length(eigenvalues)
    fdisp(fid, ['Autovalore ' num2str(eigenvalues(i)) ':']);
    if imag(eigenvalues(i)) < 0
        fdisp(fid, ['Modo: exp(' num2str(real(eigenvalues(i))) '*t) * cos(' num2str(abs(imag(eigenvalues(i)))) '*t)']);
    elseif imag(eigenvalues(i)) > 0
        fdisp(fid, ['Modo: exp(' num2str(real(eigenvalues(i))) '*t) * sin(' num2str(abs(imag(eigenvalues(i)))) '*t)']);
    else
        fdisp(fid, ['Modo: exp(' num2str(real(eigenvalues(i))) '*t)']);
    end
end


% stabilità interna
fdisp(fid, "** Stabilità interna");
fdisp(fid, "--  L'analisi della stabilità interna è finalizzata a determinare se gli stati interni del sistema tendono a convergere o divergere nel tempo.")
% -----------------------------------------------------
if all(real(eigenvalues) < 0)
    fdisp(fid, "Il sistema è internamente stabile in modo asintotico.");
elseif any(eigenvalues == 0) && rank(A) == rank(A^2) && all(real(eigenvalues) <= 0)
    fdisp(fid, "Il sistema è marginalmente stabile.");
else
    fdisp(fid, "Il sistema non è internamente stabile.");
end
fdisp(fid, "");


% raggiungibilità
fdisp(fid, "** Raggiungibilità");
fdisp(fid, "-- La raggiungibilità è un concetto complementare all'osservabilità in un sistema dinamico lineare tempo-invariante (LTI). Indica la capacità di raggiungere uno stato desiderato del sistema utilizzando i controlli disponibili.");
fdisp(fid, "-- Un sistema con matrice di stato A e matrice di ingresso B è raggiungibile se e solo se la matrice di raggiungibilità:");
fdisp(fid, "-- R = [B, AB, A^2B, ..., A^(n-1)*B]");
fdisp(fid, "-- ha rango massimo, dove n rappresenta la dimensione dello stato del sistema.");
fdisp(fid, "-- ");
% -----------------------------------------------------
% Calculate the reachability matrix
reachability_matrix = ctrb(A, B);
fdisp(fid, "reachability_matrix");
fdisp(fid, reachability_matrix);
% Check if the system is reachable
reachability_rank = rank(reachability_matrix);
if reachability_rank == size(A) && det(reachability_matrix) ~= 0
    fdisp(fid, "Il sistema è completamente raggiungibile.");
elseif reachability_rank == size(A) && det(reachability_matrix) == 0
    fdisp(fid, "Il sistema è non completamente raggiungibile.");
else
    fdisp(fid, "Il sistema non è raggiungibile. rango = ");
    fdisp(fid, reachability_rank);
end

% raggiungibilità
fdisp(fid, "** Osservabilità");
fdisp(fid,"-- L'osservabilità è una proprietà di un sistema dinamico lineare tempo-invariante (LTI) e indica la capacità di determinare lo stato del sistema utilizzando solo le misure dell'uscita. In altre parole, un sistema è osservabile se, attraverso le osservazioni dell'uscita, è possibile ricostruire il suo stato interno.");
fdisp(fid, "-- Un sistema con matrice di stato A e matrice di uscita C è osservabile se e solo se la matrice di osservabilità:");
fdisp(fid,"-- O = [C; CA; CA^2; ...; C*A^(n-1)]");
fdisp(fid,"-- ha rango massimo, dove n rappresenta la dimensione dello stato del sistema.");
% -----------------------------------------------------
% Calculate the observability matrix
observability_matrix = obsv(A, C);
fdisp(fid, 'Observability matrix:');
fdisp(fid, observability_matrix);
% Check if the system is observable
observability_rank = rank(observability_matrix);
if observability_rank == size(A) && det(observability_matrix) ~= 0
    fdisp(fid, "Il sistema è completamente osservabile.");
elseif observability_rank == size(A) && det(observability_matrix) == 0
    fdisp(fid, "Il sistema è non completamente osservabile.");
else
    fdisp(fid, "Il sistema non è osservabile. rango = ");
    fdisp(fid, observability_rank);
end


% Check the BIBO stability
fdisp(fid, "** Stabilità BIBO");
fdisp(fid, "-- Se tutti gli autovalori delle matrici di osservabilità e raggiungibilità (esclusi gli zeri dovuti al rango non massimo) hanno parte reale negativa, il sistema è considerato BIBO stabile. Ciò implica che l'effetto di un ingresso limitato sul sistema non produce risposte illimitate o instabili in uscita.");
% -----------------------------------------------------
% Calculate the eigenvalues of the observability matrix
observability_eigenvalues = eig(observability_matrix);
num_zero_observability_eigenvalues = sum(abs(observability_eigenvalues) < eps);
fdisp(fid, "observability_eigenvalues");
fdisp(fid, observability_eigenvalues);
% Calculate the eigenvalues of the reachability matrix
reachability_eigenvalues = eig(reachability_matrix);
fdisp(fid, "reachability_eigenvalues");
fdisp(fid, reachability_eigenvalues);
num_zero_reachability_eigenvalues = sum(abs(reachability_eigenvalues) < eps);
% Check BIBO stability
if all(real(observability_eigenvalues) <= 0) && all(real(reachability_eigenvalues) <= 0) && num_zero_reachability_eigenvalues == (size(A)-rank(reachability_matrix)) && num_zero_observability_eigenvalues == (size(A)-rank(observability_matrix))
    fdisp(fid,'Il sistema è BIBO stabile.');
else
    fdisp(fid,'Il sistema non è BIBO stabile.');
end