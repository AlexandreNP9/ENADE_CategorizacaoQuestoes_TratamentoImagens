from PIL import Image
import os
import sys

# Aumentar o limite para evitar o erro de decompression bomb
Image.MAX_IMAGE_PIXELS = None

def detectar_padrao_rascunho_flexivel(imagem, x_coluna, y_linha, tolerancia=5):
    """
    Detecta diferentes padrões de faixa de rascunho de forma flexível
    """
    altura = imagem.height
    
    # Padrões para rascunho: (escuro1, claro, escuro2)
    padroes_rascunho = [
        (2, 81, 2),   # Padrão principal
        (2, 80, 2),   # Possíveis variações
        (2, 82, 2),
        (3, 81, 2),
        (2, 81, 3),
        (3, 80, 3),
        (1, 81, 2),
        (2, 81, 1)
    ]
    
    for padrao in padroes_rascunho:
        escuro1, claro, escuro2 = padrao
        total_pixels = escuro1 + claro + escuro2
        
        # Verificar se temos pixels suficientes
        if y_linha + total_pixels > altura:
            continue
        
        try:
            # Primeira parte: cinza escuro
            for i in range(escuro1):
                y = y_linha + i
                pixel = imagem.getpixel((x_coluna, y))
                if not all(abs(pixel[j] - [35, 31, 32][j]) <= tolerancia for j in range(3)):
                    break
            else:
                # Segunda parte: cinza claro
                for i in range(claro):
                    y = y_linha + escuro1 + i
                    pixel = imagem.getpixel((x_coluna, y))
                    if not all(abs(pixel[j] - [211, 210, 210][j]) <= tolerancia for j in range(3)):
                        break
                else:
                    # Terceira parte: cinza escuro
                    for i in range(escuro2):
                        y = y_linha + escuro1 + claro + i
                        pixel = imagem.getpixel((x_coluna, y))
                        if not all(abs(pixel[j] - [35, 31, 32][j]) <= tolerancia for j in range(3)):
                            break
                    else:
                        # Padrão encontrado!
                        return padrao
        
        except Exception:
            continue
    
    return None

def encontrar_inicio_rascunho(imagem):
    """
    Encontra a posição Y onde começa a área de rascunho
    analisando o centro da imagem
    """
    altura = imagem.height
    largura = imagem.width
    
    # Analisar no centro da imagem (metade da largura)
    x_coluna = largura // 2
    
    # Procurar pela faixa de rascunho em cada linha Y
    # Começar a busca mais para baixo, já que o rascunho geralmente vem no final
    y_inicio_busca = altura // 2  # Começar na metade
    y = y_inicio_busca
    
    while y < altura - 100:  # Deixar margem para o padrão
        padrao = detectar_padrao_rascunho_flexivel(imagem, x_coluna, y)
        
        if padrao:
            return y, padrao
        
        y += 1
    
    return None, None

def recortar_rascunho_imagem(caminho_imagem, pasta_saida):
    """
    Recorta a área de rascunho de uma imagem específica
    Corta 1 pixel acima do início da faixa
    """
    
    if not os.path.exists(caminho_imagem):
        print(f"❌ Imagem '{caminho_imagem}' não encontrada!")
        return False
    
    try:
        with Image.open(caminho_imagem) as img:
            nome_arquivo = os.path.basename(caminho_imagem)
            
            # Encontrar onde começa o rascunho
            inicio_rascunho, padrao = encontrar_inicio_rascunho(img)
            
            if inicio_rascunho is None:
                # Se não encontrou rascunho, copiar a imagem original
                caminho_saida = os.path.join(pasta_saida, nome_arquivo)
                img.save(caminho_saida)
                print(f"    ➡ {nome_arquivo} - Sem rascunho (cópia)")
                return False
            
            # Cortar 1 pixel acima do início da faixa
            corte_y = max(0, inicio_rascunho - 1)
            
            # Recortar até o início do rascunho
            area_recorte = (0, 0, img.width, corte_y)
            img_recortada = img.crop(area_recorte)
            
            # Salvar a imagem recortada (sobrescrever ou criar novo nome)
            caminho_saida = os.path.join(pasta_saida, nome_arquivo)
            img_recortada.save(caminho_saida)
            
            altura_original = img.height
            altura_recortada = img_recortada.height
            pixels_removidos = altura_original - altura_recortada
            
            print(f"    ✓ {nome_arquivo} - Rascunho removido: {altura_original}px → {altura_recortada}px (-{pixels_removidos}px) [padrão {padrao}]")
            return True
                
    except Exception as e:
        print(f"✗ ERRO ao processar {caminho_imagem}: {e}")
        return False

def processar_pasta_questoes(pasta_entrada, pasta_saida):
    """
    Processa todas as imagens de uma pasta, removendo rascunho quando encontrado
    """
    if not os.path.exists(pasta_entrada):
        print(f"❌ Pasta de entrada '{pasta_entrada}' não encontrada!")
        return
    
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)
    
    arquivos_processados = 0
    arquivos_com_rascunho = 0
    
    print(f"📁 Processando pasta: {os.path.abspath(pasta_entrada)}")
    print(f"💾 Salvando em: {os.path.abspath(pasta_saida)}")
    print("-" * 60)
    
    for arquivo in os.listdir(pasta_entrada):
        if arquivo.lower().endswith('.png'):
            caminho_imagem = os.path.join(pasta_entrada, arquivo)
            
            tem_rascunho = recortar_rascunho_imagem(caminho_imagem, pasta_saida)
            arquivos_processados += 1
            
            if tem_rascunho:
                arquivos_com_rascunho += 1
    
    print("\n" + "=" * 60)
    print("RELATÓRIO DE REMOÇÃO DE RASCUNHO")
    print("=" * 60)
    print(f"Imagens processadas: {arquivos_processados}")
    print(f"Imagens com rascunho: {arquivos_com_rascunho}")
    print(f"Imagens sem rascunho: {arquivos_processados - arquivos_com_rascunho}")
    
    if arquivos_processados == 0:
        print("⚠  Nenhuma imagem PNG encontrada na pasta!")
    else:
        print(f"\n🎉 Processamento concluído!")

def main():
    # CONFIGURAÇÃO: 
    pasta_entrada = "."  # Pasta com as questões já recortadas
    pasta_saida = "questoes_sem_rascunho"  # Pasta para salvar as questões sem rascunho
    
    print("✂️  Iniciando remoção de área de rascunho das questões...")
    print("=" * 60)
    print("Padrões procurados (vertical):")
    print("  • 2px(35,31,32) + 81px(211,210,210) + 2px(35,31,32)")
    print("  • E outras variações...")
    print("Análise: Coluna do centro da imagem")
    print("Corte: 1 pixel acima do início da faixa")
    print("=" * 60)
    
    processar_pasta_questoes(pasta_entrada, pasta_saida)

if __name__ == "__main__":
    main()