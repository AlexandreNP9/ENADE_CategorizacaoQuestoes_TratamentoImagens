from PIL import Image
import os
import sys

def unir_paginas_inteiras_verticalmente(pasta_entrada, pasta_saida):
    """
    Une verticalmente todas as imagens de página inteira
    (que não foram cortadas em colunas)
    """
    
    print(f"Coletando imagens de página inteira de: {os.path.abspath(pasta_entrada)}")
    print(f"Salvando em: {os.path.abspath(pasta_saida)}")
    print("-" * 60)
    
    # Coletar todas as imagens de página inteira (que não são colunas)
    imagens_por_pasta = {}
    
    for pasta_raiz, pastas, arquivos in os.walk(pasta_entrada):
        for arquivo in arquivos:
            if arquivo.lower().endswith('.png'):
                # Ignorar imagens que são colunas
                if '_esquerda.png' in arquivo or '_direita.png' in arquivo:
                    continue
                    
                relativo_path = os.path.relpath(pasta_raiz, pasta_entrada)
                
                if relativo_path not in imagens_por_pasta:
                    imagens_por_pasta[relativo_path] = []
                
                caminho_imagem = os.path.join(pasta_raiz, arquivo)
                imagens_por_pasta[relativo_path].append(caminho_imagem)
    
    total_unioes = 0
    erros = 0
    
    for pasta_relativa, imagens_list in imagens_por_pasta.items():
        if not imagens_list:
            continue
            
        # Ordenar as imagens por nome para manter a sequência correta
        imagens_ordenadas = sorted(imagens_list)
        
        try:
            # Abrir todas as imagens
            imagens_abertas = [Image.open(img_path) for img_path in imagens_ordenadas]
            
            # Calcular dimensões da imagem final
            largura = max(img.width for img in imagens_abertas)
            altura_total = sum(img.height for img in imagens_abertas)
            
            # Criar nova imagem
            imagem_final = Image.new('RGB', (largura, altura_total), 'white')
            
            # Colar cada imagem verticalmente
            y_offset = 0
            for i, img in enumerate(imagens_abertas):
                x_offset = (largura - img.width) // 2  # Centralizar se larguras diferentes
                imagem_final.paste(img, (x_offset, y_offset))
                y_offset += img.height
            
            # Criar pasta de destino
            pasta_destino = os.path.join(pasta_saida, pasta_relativa)
            if not os.path.exists(pasta_destino):
                os.makedirs(pasta_destino)
            
            # Salvar imagem final
            nome_arquivo = "paginas_inteiras_unidas.png"
            caminho_final = os.path.join(pasta_destino, nome_arquivo)
            imagem_final.save(caminho_final)
            
            total_unioes += 1
            print(f"✓ {pasta_relativa} - Uniu {len(imagens_ordenadas)} páginas → {largura}x{altura_total}")
            
            # Fechar imagens
            for img in imagens_abertas:
                img.close()
                
        except Exception as e:
            erros += 1
            print(f"✗ ERRO ao unir {pasta_relativa}: {e}")
    
    print("\n" + "=" * 60)
    print("RELATÓRIO DE UNIÃO VERTICAL - PÁGINAS INTEIRAS")
    print("=" * 60)
    print(f"Pastas processadas: {len(imagens_por_pasta)}")
    print(f"Uniões realizadas: {total_unioes}")
    print(f"Erros: {erros}")
    
    if total_unioes == 0:
        print("\n⚠  Nenhuma união foi realizada!")
        print("   Verifique se existem imagens de página inteira (sem '_esquerda' ou '_direita' no nome)")
    elif erros == 0:
        print("\n🎉 Todas as uniões de páginas inteiras foram realizadas com sucesso!")
    else:
        print(f"\n⚠  {erros} união(ões) tiveram erro no processamento.")

def main():
    pasta_entrada = "ImagensPaginaToda"
    pasta_saida = "."
    
    if not os.path.exists(pasta_entrada):
        print(f"❌ Pasta de entrada '{pasta_entrada}' não encontrada!")
        print("   Execute primeiro o passo de remover bordas")
        sys.exit(1)
    
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)
    
    print("🔄 Iniciando união vertical das páginas inteiras...")
    print("=" * 60)
    
    unir_paginas_inteiras_verticalmente(pasta_entrada, pasta_saida)
    
    print("\n✅ União vertical das páginas inteiras finalizada!")

if __name__ == "__main__":
    main()