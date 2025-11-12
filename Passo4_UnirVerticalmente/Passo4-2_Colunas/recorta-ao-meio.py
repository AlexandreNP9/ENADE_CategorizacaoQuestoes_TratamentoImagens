from PIL import Image
import os
import sys

def cortar_imagens_ao_meio(pasta_entrada, pasta_saida):
    """
    Corta cada imagem PNG ao meio verticalmente
    
    Args:
        pasta_entrada: Pasta com as imagens originais
        pasta_saida: Pasta para salvar as imagens cortadas
    """
    
    total_imagens = 0
    imagens_processadas = 0
    erros = 0
    
    print(f"Processando imagens de: {os.path.abspath(pasta_entrada)}")
    print(f"Salvando em: {os.path.abspath(pasta_saida)}")
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
                
                try:
                    with Image.open(caminho_entrada) as img:
                        largura, altura = img.size
                        
                        ponto_meio = largura // 2
                        
                        esquerda = img.crop((0, 0, ponto_meio, altura))
                        direita = img.crop((ponto_meio, 0, largura, altura))
                        
                        nome_base = arquivo.replace('.png', '')
                        
                        caminho_esquerda = os.path.join(pasta_destino, f"{nome_base}_esquerda.png")
                        caminho_direita = os.path.join(pasta_destino, f"{nome_base}_direita.png")
                        
                        esquerda.save(caminho_esquerda)
                        direita.save(caminho_direita)
                        
                        imagens_processadas += 1
                        print(f"✓ {arquivo} - {largura}x{altura} → Esquerda: {ponto_meio}x{altura}, Direita: {largura - ponto_meio}x{altura}")
                        
                except Exception as e:
                    erros += 1
                    print(f"✗ ERRO ao processar {arquivo}: {e}")
    
    print("\n" + "=" * 60)
    print("RELATÓRIO DE CORTE AO MEIO")
    print("=" * 60)
    print(f"Imagens encontradas: {total_imagens}")
    print(f"Imagens processadas: {imagens_processadas}")
    print(f"Total de metades geradas: {imagens_processadas * 2}")
    print(f"Erros: {erros}")
    
    if total_imagens == 0:
        print("\n⚠  Nenhuma imagem PNG encontrada!")
    elif erros == 0:
        print("\n🎉 Todas as imagens foram cortadas com sucesso!")
    else:
        print(f"\n⚠  {erros} imagem(ns) tiveram erro no processamento.")

def main():
    pasta_entrada = "ImagensColunas"
    pasta_saida = "Recortadas"
    
    if not os.path.exists(pasta_entrada):
        print(f"❌ Pasta de entrada '{pasta_entrada}' não encontrada!")
        print("   Execute primeiro o passo de remoção de bordas")
        sys.exit(1)
    
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)
    
    print("✂️  Iniciando corte das imagens ao meio...")
    print("=" * 60)
    
    cortar_imagens_ao_meio(pasta_entrada, pasta_saida)
    
    print("\n✅ Corte ao meio finalizado!")

if __name__ == "__main__":
    main()