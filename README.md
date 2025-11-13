# ENADE_CategorizacaoQuestoes_TratamentoImagens
Conversão do PDF para PNG e tratamentos pontuais para usar no próximo repositório.

# Softwares utilizados
Linux Mint 22.1  
Python 3  
Pillow  
Poppler-utils  
gThumb  
GIMP 2.10

# Instalar softwares
Espera-se que já tenha o python3 instalado

## Variável de Ambiente (caso necessário)
python3 -m venv venv  
source venv/bin/activate  

## Poppler
sudo apt-get install poppler-utils

## Biblioteca PDF2Image e dependências
pip3 install pdf2image pillow  

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
