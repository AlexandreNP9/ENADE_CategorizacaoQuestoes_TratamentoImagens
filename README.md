# ENADE_CategorizacaoQuestoes_TratamentoImagens
Projeto para categorização das questões do ENADE de acordo com os descritores e habilidades previstas nas [Diretrizes Curriculares Nacionais (DNCs)](https://www.gov.br/mec/pt-br/cne/normas-classificadas-por-assunto/diretrizes-curriculares-cursos-de-graduacao).
Este repositório faz parte de um projeto com subsistemas distribuído.

Repositório Geral:
https://github.com/AlexandreNP9/ENADE_CategorizacaoQuestoes_GERAL

# Objetivos deste repositório
Converter PDF para PNG  
Recortar as questões para que tenha uma questão por imagem  
Remover excessos  
Renomear as imagens  

# Especifidades técnicas
## Programas e bibliotecas utilziadas
Linux Mint 22.1
Python 3  
gthumb  
os  
pdf2image  
pillow  

# Antes de executar o código
## Criar variável de ambiente
```
python3 -m venv venv  
source venv/bin/activate  
```

## Instalar o pdf2image
```
pip3 install pdf2image  
```

## Executar os códigos nas pastas
Cada pasta tem códigos ou instruções específicas

# Passo a Passo
Passo 1) Reunir os PDFs para trabalhar  
Passo 2) Converter os PDFs em PNGs  
Passo 3) Remover as bordas externas (margens) das imagens das questões da prova  
Passo 4) Unir verticalmente as imagens:  
Passo 4.1) Questões ocupam todo o espaço horizontal da página  
Passo 4.2) Questões ocupam duas colunas em uma página:  
Passo 4.2.1) Cortar ao meio as imagens em que as questões ocupam duas colunas em uma página  
Passo 4.2.2) Remover bordas internas dessas colunas  
Passo 4.2.3) Unir verticalmente das colunas  
Passo 5) Recortar por questões
Passo 5.1) Percorrer as imagens unidas verticalmente (imagem das questões de página inteira e imagem das questões de colunas) e recortar no início de cada questão  
Passo 5.2) Remover imagens de "Área livre". Fiz manualmente.  
Passo 5.3) Percorrer as imagens para remover os "Rascunho"  
Passo 6) Renomear imagens com os nomes das questões. Fiz manualmente.  
Passo 7) Tratar qualquer situação manualmente  
