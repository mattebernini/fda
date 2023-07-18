pkg load control

% INPUT
fid = fopen('website/static/teoria/files/in_matrici.txt', 'r');
combined_matrix = textscan(fid, '%s', 'Delimiter', '');
fclose(fid);

A = str2num(combined_matrix{1}{1});
B = str2num(combined_matrix{1}{2});
C = str2num(combined_matrix{1}{3});
D = str2num(combined_matrix{1}{4});

fid = fopen("website/static/teoria/files/result.txt", "w");

% analisi modale
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
fdisp(fid, "");

% stabilità interna
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
% -----------------------------------------------------
% Calculate the reachability matrix
reachability_matrix = ctrb(A, B);
fdisp(fid, "Mr = ");
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
fdisp(fid, "");

% raggiungibilità
% -----------------------------------------------------
% Calculate the observability matrix
observability_matrix = obsv(A, C);
fdisp(fid, "Mo = ");
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
fdisp(fid, "");



