from PIL import Image
import os
import sys

# Aumentar o limite para evitar o erro de decompression bomb
Image.MAX_IMAGE_PIXELS = None

def detectar_padrao_flexivel(imagem, x_coluna, y_linha, tolerancia=5):
    """
    Detecta diferentes padrões de faixa de questão de forma flexível
    """
    altura = imagem.height
    
    # Padrões conhecidos: (cinza_claro1, cinza_escuro, cinza_claro2)
    padroes = [ #Possíveis variações
        (14, 2, 14),
        (14, 2, 15),
        (14, 2, 16),
        (14, 2, 17),
        
        (14, 3, 14),
        (14, 3, 15),
        (14, 3, 16),
        (14, 3, 17),

        (14, 4, 14),
        (14, 4, 15),
        (14, 4, 16),
        (14, 4, 17),

        (15, 2, 14),
        (15, 2, 15),
        (15, 2, 16),
        (15, 2, 17),
        
        (15, 3, 14),
        (15, 3, 15),
        (15, 3, 16),
        (15, 3, 17),

        (15, 4, 14),
        (15, 4, 15),
        (15, 4, 16),
        (15, 4, 17),

        (16, 2, 14),
        (16, 2, 15),
        (16, 2, 16),
        (16, 2, 17),
        
        (16, 3, 14),
        (16, 3, 15),
        (16, 3, 16),
        (16, 3, 17),

        (16, 4, 14),
        (16, 4, 15),
        (16, 4, 16),
        (16, 4, 17)
    ]
    
    for padrao in padroes:
        claro1, escuro, claro2 = padrao
        total_pixels = claro1 + escuro + claro2
        
        # Verificar se temos pixels suficientes
        if y_linha + total_pixels > altura:
            continue
        
        try:
            # Primeira parte: cinza claro
            for i in range(claro1):
                y = y_linha + i
                pixel = imagem.getpixel((x_coluna, y))
                if not all(abs(pixel[j] - [211, 210, 210][j]) <= tolerancia for j in range(3)):
                    break
            else:
                # Segunda parte: cinza escuro
                for i in range(escuro):
                    y = y_linha + claro1 + i
                    pixel = imagem.getpixel((x_coluna, y))
                    if not all(abs(pixel[j] - [35, 31, 32][j]) <= tolerancia for j in range(3)):
                        break
                else:
                    # Terceira parte: cinza claro
                    for i in range(claro2):
                        y = y_linha + claro1 + escuro + i
                        pixel = imagem.getpixel((x_coluna, y))
                        if not all(abs(pixel[j] - [211, 210, 210][j]) <= tolerancia for j in range(3)):
                            break
                    else:
                        # Padrão encontrado!
                        return padrao
        
        except Exception:
            continue
    
    return None

def detectar_faixa_questao_na_coluna(imagem, x_coluna, y_linha, tolerancia=5):
    """
    Detecta se na posição (x_coluna, y_linha) existe alguma faixa de questão
    usando os padrões flexíveis
    """
    padrao = detectar_padrao_flexivel(imagem, x_coluna, y_linha, tolerancia)
    return padrao is not None

def encontrar_inicios_questoes(imagem):
    """
    Encontra todas as posições Y onde começam as questões
    usando uma coluna específica (penúltimo pixel da direita)
    """
    altura = imagem.height
    largura = imagem.width
    inicios = []
    padroes_encontrados = []
    
    # Usar o penúltimo pixel da direita como coluna de análise
    x_coluna = largura - 2
    
    print(f"    Analisando coluna X={x_coluna} (penúltimo da direita)")
    print(f"    Procurando faixas de questão na imagem {altura}px de altura...")
    
    # Procurar pela faixa em cada linha Y
    y = 0
    while y < altura - 50:  # Deixar margem para o maior padrão possível
        padrao = detectar_padrao_flexivel(imagem, x_coluna, y)
        
        if padrao:
            # Encontrou uma faixa, recuar 10 pixels para o início da questão
            inicio_questao = max(0, y - 10)
            inicios.append(inicio_questao)
            padroes_encontrados.append(padrao)
            print(f"      ✓ Questão {len(inicios)}: Y={y}, padrão {padrao}, recorte em Y={inicio_questao}")
            # Pular algumas linhas para evitar detectar a mesma faixa múltiplas vezes
            y += 100
        else:
            y += 1
    
    # Relatório dos padrões encontrados
    if padroes_encontrados:
        print(f"\n    📊 Padrões encontrados:")
        from collections import Counter
        contador = Counter(padroes_encontrados)
        for padrao, count in contador.items():
            print(f"       {padrao}: {count} questão(ões)")
    
    return inicios

def recortar_questoes_imagem(caminho_imagem, pasta_saida):
    """
    Recorta uma imagem específica nas posições onde começam as questões
    """
    
    print(f"Processando imagem: {os.path.abspath(caminho_imagem)}")
    print(f"Salvando questões recortadas em: {os.path.abspath(pasta_saida)}")
    print("-" * 60)
    
    if not os.path.exists(caminho_imagem):
        print(f"❌ Imagem '{caminho_imagem}' não encontrada!")
        return
    
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)
    
    total_questoes = 0
    
    try:
        with Image.open(caminho_imagem) as img:
            nome_arquivo = os.path.basename(caminho_imagem)
            print(f"📄 Processando: {nome_arquivo} ({img.width}x{img.height})")
            
            # Encontrar onde começam as questões
            inicios = encontrar_inicios_questoes(img)
            
            if not inicios:
                print(f"    ⚠  Nenhuma questão encontrada na imagem")
                return
            
            # Adicionar o final da imagem como último corte
            inicios.append(img.height)
            
            # Recortar cada questão
            for i in range(len(inicios) - 1):
                y_inicio = inicios[i]
                y_fim = inicios[i + 1]
                
                # Recortar a questão
                area_recorte = (0, y_inicio, img.width, y_fim)
                questao_img = img.crop(area_recorte)
                
                # Salvar a questão
                nome_base = os.path.splitext(nome_arquivo)[0]
                nome_questao = f"{nome_base}_questao_{i+1:02d}.png"
                caminho_questao = os.path.join(pasta_saida, nome_questao)
                questao_img.save(caminho_questao)
                
                altura_questao = y_fim - y_inicio
                print(f"    ✓ Questão {i+1} recortada: {altura_questao}px")
                total_questoes += 1
                
    except Exception as e:
        print(f"✗ ERRO ao processar imagem: {e}")
        return
    
    print(f"\n✅ Recorte concluído: {total_questoes} questões recortadas!")
    return total_questoes

def main():
    # CONFIGURAÇÃO: Altere aqui conforme necessário
    caminho_imagem = "paginas_inteiras_unidas.png"  # Ou "colunas_unidas.png" ou "paginas_inteiras_unidas.png"
    pasta_saida = "paginas_inteiras_unidas"
    
    print("✂️  Iniciando recorte automático de questões...")
    print("=" * 60)
    print("Padrões procurados (vertical):")
    print("  • 10px(211,210,210) + 3px(35,31,32) + 10px(211,210,210)")
    print("  • 10px(211,210,210) + 2px(35,31,32) + 16px(211,210,210)")
    print("  • E outras variações...")
    print("Análise: Coluna do penúltimo pixel da direita")
    print("Recorte: 10px acima do início da faixa")
    print("=" * 60)
    
    total_questoes = recortar_questoes_imagem(caminho_imagem, pasta_saida)
    
    if total_questoes == 0:
        print("\n⚠  Nenhuma questão foi recortada!")
        print("   Verifique:")
        print("   - Se o caminho da imagem está correto")
        print("   - Se as faixas de questão seguem algum dos padrões")
        print("   - Se a imagem tem o formato esperado")

if __name__ == "__main__":
    main()