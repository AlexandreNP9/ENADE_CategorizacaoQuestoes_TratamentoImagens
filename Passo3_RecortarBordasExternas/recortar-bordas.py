from PIL import Image
import os
import sys

def remover_bordas_imagens(pasta_entrada, pasta_saida, cortes):
    total_imagens = 0
    imagens_processadas = 0
    erros = 0
    
    print(f"Processando imagens de: {os.path.abspath(pasta_entrada)}")
    print(f"Salvando em: {os.path.abspath(pasta_saida)}")
    print(f"Cortes: Topo={cortes['topo']}px, Base={cortes['base']}px, Esquerda={cortes['esquerda']}px, Direita={cortes['direita']}px")
    print("-" * 60)
    
    for pasta_raiz, pastas, arquivos in os.walk(pasta_entrada):
        for arquivo in arquivos:
            if arquivo.lower().endswith('.png'):
                caminho_entrada = os.path.join(pasta_raiz, arquivo)
                total_imagens += 1
                
                relativo_path = os.path.relpath(pasta_raiz, pasta_entrada)
                pasta_destino = os.path.join(pasta_saida, relativo_path)
                
                if not os.path.exists(pasta_destino):
                    os.makedirs(pasta_destino)
                
                caminho_saida = os.path.join(pasta_destino, arquivo)
                
                try:
                    with Image.open(caminho_entrada) as img:
                        largura, altura = img.size
                        
                        novo_largura = largura - cortes['esquerda'] - cortes['direita']
                        novo_altura = altura - cortes['topo'] - cortes['base']
                        
                        if novo_largura <= 0 or novo_altura <= 0:
                            print(f"⚠  Aviso: Imagem {arquivo} muito pequena para os cortes especificados")
                            continue
                        
                        area_corte = (
                            cortes['esquerda'],    # left
                            cortes['topo'],        # top
                            largura - cortes['direita'],  # right
                            altura - cortes['base']       # bottom
                        )
                        
                        img_cortada = img.crop(area_corte)
                        img_cortada.save(caminho_saida)
                        
                        imagens_processadas += 1
                        print(f"✓ {arquivo} - Original: {largura}x{altura} → Cortada: {novo_largura}x{novo_altura}")
                        
                except Exception as e:
                    erros += 1
                    print(f"✗ ERRO ao processar {arquivo}: {e}")
    
    print("\n" + "=" * 60)
    print("RELATÓRIO DE REMOÇÃO DE BORDAS")
    print("=" * 60)
    print(f"Imagens encontradas: {total_imagens}")
    print(f"Imagens processadas: {imagens_processadas}")
    print(f"Erros: {erros}")
    
    if total_imagens == 0:
        print("\n⚠  Nenhuma imagem PNG encontrada!")
    elif erros == 0:
        print("\n🎉 Todas as imagens foram processadas com sucesso!")
    else:
        print(f"\n⚠  {erros} imagem(ns) tiveram erro no processamento.")

def main():
    pasta_entrada = "../Passo2_ConverterPDFs/2021/BachareladoCienciaDaComputacao_Prova"
    pasta_saida = "."
    
    cortes = {
        'topo': 330,      # 330 pixels da margem superior
        'base': 151,      # 151 pixels da margem inferior
        'esquerda': 125,  # 125 pixels da margem esquerda
        'direita': 125    # 125 pixels da margem direita
    }
    
    if not os.path.exists(pasta_entrada):
        print(f"❌ Pasta de entrada '{pasta_entrada}' não encontrada!")
        print("   Execute primeiro o passo de conversão PDF→PNG")
        sys.exit(1)
    
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)
    
    print("🔪 Iniciando remoção de bordas das imagens...")
    print("=" * 60)
    
    remover_bordas_imagens(pasta_entrada, pasta_saida, cortes)
    
    print("\n✅ Remoção de bordas finalizada!")

if __name__ == "__main__":
    main()