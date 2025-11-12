from PIL import Image
import os
import sys

def remover_bordas_internas(pasta_entrada, pasta_saida):
    """
    Remove bordas internas das colunas:
    - 25px da direita nas imagens _esquerda.png
    - 25px da esquerda nas imagens _direita.png
    """
    
    total_imagens = 0
    imagens_processadas = 0
    erros = 0
    
    print(f"Processando imagens de: {os.path.abspath(pasta_entrada)}")
    print(f"Salvando em: {os.path.abspath(pasta_saida)}")
    print("Removendo 25px da borda interna de cada coluna")
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
                        
                        if arquivo.endswith('_esquerda.png'):
                            # Remove 25px da direita
                            nova_largura = largura - 25
                            if nova_largura <= 0:
                                print(f"⚠  Aviso: Imagem {arquivo} muito pequena para corte")
                                continue
                            
                            area_corte = (0, 0, nova_largura, altura)
                            img_cortada = img.crop(area_corte)
                            img_cortada.save(caminho_saida)
                            
                            imagens_processadas += 1
                            print(f"✓ {arquivo} - Removeu 25px da direita: {largura}x{altura} → {nova_largura}x{altura}")
                            
                        elif arquivo.endswith('_direita.png'):
                            # Remove 25px da esquerda
                            nova_largura = largura - 25
                            if nova_largura <= 0:
                                print(f"⚠  Aviso: Imagem {arquivo} muito pequena para corte")
                                continue
                            
                            area_corte = (25, 0, largura, altura)
                            img_cortada = img.crop(area_corte)
                            img_cortada.save(caminho_saida)
                            
                            imagens_processadas += 1
                            print(f"✓ {arquivo} - Removeu 25px da esquerda: {largura}x{altura} → {nova_largura}x{altura}")
                            
                        else:
                            # Copia imagens que não são colunas (caso existam)
                            img.save(caminho_saida)
                            print(f"➡ {arquivo} - Copiada sem alterações")
                            
                except Exception as e:
                    erros += 1
                    print(f"✗ ERRO ao processar {arquivo}: {e}")
    
    print("\n" + "=" * 60)
    print("RELATÓRIO DE REMOÇÃO DE BORDAS INTERNAS")
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
    pasta_entrada = "Recortadas"
    pasta_saida = "SemBordasInternas"
    
    if not os.path.exists(pasta_entrada):
        print(f"❌ Pasta de entrada '{pasta_entrada}' não encontrada!")
        print("   Execute primeiro o passo de cortar ao meio")
        sys.exit(1)
    
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)
    
    print("🔧 Iniciando remoção de bordas internas...")
    print("=" * 60)
    
    remover_bordas_internas(pasta_entrada, pasta_saida)
    
    print("\n✅ Remoção de bordas internas finalizada!")

if __name__ == "__main__":
    main()