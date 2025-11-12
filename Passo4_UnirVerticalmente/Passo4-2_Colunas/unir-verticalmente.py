from PIL import Image
import os
import sys

def unir_colunas_verticalmente(pasta_entrada, pasta_saida):
    """
    Une verticalmente as colunas na ordem:
    - Lado esquerdo da página 1
    - Lado direito da página 1
    - Lado esquerdo da página 2
    - Lado direito da página 2
    - E assim por diante...
    """
    
    print(f"Coletando imagens de: {os.path.abspath(pasta_entrada)}")
    print(f"Salvando em: {os.path.abspath(pasta_saida)}")
    print("Ordem de união: esquerda_pag1 → direita_pag1 → esquerda_pag2 → direita_pag2 → ...")
    print("-" * 60)
    
    # Coletar todas as imagens organizadas por pasta e número de página
    imagens_por_pasta = {}
    
    for pasta_raiz, pastas, arquivos in os.walk(pasta_entrada):
        for arquivo in arquivos:
            if arquivo.lower().endswith('.png'):
                relativo_path = os.path.relpath(pasta_raiz, pasta_entrada)
                
                if relativo_path not in imagens_por_pasta:
                    imagens_por_pasta[relativo_path] = {'esquerda': [], 'direita': []}
                
                caminho_imagem = os.path.join(pasta_raiz, arquivo)
                
                if arquivo.endswith('_esquerda.png'):
                    imagens_por_pasta[relativo_path]['esquerda'].append(caminho_imagem)
                elif arquivo.endswith('_direita.png'):
                    imagens_por_pasta[relativo_path]['direita'].append(caminho_imagem)
    
    total_unioes = 0
    erros = 0
    
    for pasta_relativa, imagens in imagens_por_pasta.items():
        esquerda_list = sorted(imagens['esquerda'])
        direita_list = sorted(imagens['direita'])
        
        if not esquerda_list and not direita_list:
            continue
        
        # Verificar se temos o mesmo número de imagens esquerda e direita
        if len(esquerda_list) != len(direita_list):
            print(f"⚠  Aviso: Número diferente de colunas em {pasta_relativa}")
            print(f"   Esquerda: {len(esquerda_list)}, Direita: {len(direita_list)}")
        
        num_paginas = min(len(esquerda_list), len(direita_list))
        
        if num_paginas == 0:
            continue
        
        # Criar lista na ordem correta: esq1, dir1, esq2, dir2, ...
        imagens_ordenadas = []
        for i in range(num_paginas):
            imagens_ordenadas.append(esquerda_list[i])
            imagens_ordenadas.append(direita_list[i])
        
        # Juntar todas as imagens verticalmente
        try:
            imagens_abertas = [Image.open(img_path) for img_path in imagens_ordenadas]
            
            # Calcular dimensões da imagem final
            largura = max(img.width for img in imagens_abertas)
            altura_total = sum(img.height for img in imagens_abertas)
            
            # Criar nova imagem
            imagem_final = Image.new('RGB', (largura, altura_total), 'white')
            
            # Colar cada imagem
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
            nome_arquivo = "colunas_unidas.png"
            caminho_final = os.path.join(pasta_destino, nome_arquivo)
            imagem_final.save(caminho_final)
            
            total_unioes += 1
            print(f"✓ {pasta_relativa} - Uniu {len(imagens_ordenadas)} colunas → {largura}x{altura_total}")
            
            # Fechar imagens
            for img in imagens_abertas:
                img.close()
                
        except Exception as e:
            erros += 1
            print(f"✗ ERRO ao unir {pasta_relativa}: {e}")
    
    print("\n" + "=" * 60)
    print("RELATÓRIO DE UNIÃO VERTICAL")
    print("=" * 60)
    print(f"Pastas processadas: {len(imagens_por_pasta)}")
    print(f"Uniões realizadas: {total_unioes}")
    print(f"Erros: {erros}")
    
    if total_unioes == 0:
        print("\n⚠  Nenhuma união foi realizada!")
    elif erros == 0:
        print("\n🎉 Todas as uniões foram realizadas com sucesso!")
    else:
        print(f"\n⚠  {erros} união(ões) tiveram erro no processamento.")

def main():
    pasta_entrada = "SemBordasInternas"
    pasta_saida = "."
    
    if not os.path.exists(pasta_entrada):
        print(f"❌ Pasta de entrada '{pasta_entrada}' não encontrada!")
        print("   Execute primeiro o passo de remover bordas internas")
        sys.exit(1)
    
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)
    
    print("🔄 Iniciando união vertical das colunas...")
    print("=" * 60)
    
    unir_colunas_verticalmente(pasta_entrada, pasta_saida)
    
    print("\n✅ União vertical finalizada!")

if __name__ == "__main__":
    main()