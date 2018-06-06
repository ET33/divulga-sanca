# Guia para utilização do "[Projeto][projects]" deste repositório (note que "Projeto" significa o quadro Kanban do Projeto)
US - _User Stories_

## Criando uma US dentro do Projeto (Kanban)
* Cada Projeto representará uma Sprint, nomeados com o padrão: Sprint1, Sprint2, Sprint3, ...
* Dentro do projeto, existem 2 tipos de objetos que são colocados em cada coluna: Cards e Notes
* Os Cards representarão US.
* As Notes não possuem definição por enquanto
* Para criar uma US, você deverá criar uma [_Issue_][about issues], e existem duas formas de fazer isso:
  * [Criar uma Issue a partir da página de Issues][creating issues]
  * Criar uma Note na coluna dos Projetos, e promovê-la a uma Issue
* Para quebrar a US em microtarefas, entre nos detalhes de uma Issue e edite (ou peça para o dono da Issue) o primeiro comentário da seguinte maneira:
```
- [X] tarefa 1
- [ ] tarefa 2
- [ ] tarefa 3
...
```
O resultado será da seguinte maneira:
- [X] tarefa 1
- [ ] tarefa 2
- [ ] tarefa 3
...

## Realizando a US
Para realizar uma US, sigamos o seguinte padrão: uma branch por US (feature)
* Crie uma nova branch, com um nome reduzido e expressivo da US
* Certifique-se que também foi criada a branch no repositório do GitHub (origin)
* Ao finalizar a US, faça o `git push` para a branch de mesmo nome no GitHub
* Crie um [Pull Request][], atribuindo para ao menos uma pessoa rever o que foi feito
* Após a aprovação, finalize o Pull Request com o Merge para a master

[about issues]: https://help.github.com/articles/about-issues
[creating issues]: https://help.github.com/articles/creating-an-issue
[pull request]: https://github.com/ET33/divulga-sanca/pulls
[projects]: https://github.com/ET33/divulga-sanca/projects
