pkg load control

A = input("A = ");

fid = fopen("website/static/teoria/files/result.txt", "w");

[eigenvectors, eigenvalues] = eig(A);
eigenvalues = diag(eigenvalues);
for i = 1:length(eigenvalues)
    fdisp(fid, ['Autovalore: ' num2str(eigenvalues(i))]);
    if imag(eigenvalues(i)) < 0
        fdisp(fid, ['Modo: exp(' num2str(real(eigenvalues(i))) '*t) * cos(' num2str(abs(imag(eigenvalues(i)))) '*t)']);
    elseif imag(eigenvalues(i)) > 0
        fdisp(fid, ['Modo: exp(' num2str(real(eigenvalues(i))) '*t) * sin(' num2str(abs(imag(eigenvalues(i)))) '*t)']);
    else
        fdisp(fid, ['Modo: exp(' num2str(real(eigenvalues(i))) '*t)']);
    end
end


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