from pdf2image import convert_from_path
import os
import sys

def verificar_pre_requisitos():
    try:
        from pdf2image import convert_from_path
        from PIL import Image
        return True
    except ImportError as e:
        print(f"ERRO: Biblioteca não encontrada: {e}")
        print("\nInstale as dependências:")
        print("pip install pdf2image pillow")
        print("\nNo Ubuntu/Debian:")
        print("sudo apt-get install poppler-utils")
        return False

def converter_pdfs_para_png(pasta_entrada, pasta_saida, resolucao_dpi=300):
    total_pdfs = 0
    total_paginas = 0
    pdfs_com_erro = 0
    
    print(f"Buscando PDFs em: {os.path.abspath(pasta_entrada)}")
    print(f"Salvando PNGs em: {os.path.abspath(pasta_saida)}")
    print("-" * 60)
    
    for pasta_raiz, pastas, arquivos in os.walk(pasta_entrada):
        for arquivo in arquivos:
            if arquivo.lower().endswith('.pdf'):
                caminho_pdf = os.path.join(pasta_raiz, arquivo)
                total_pdfs += 1
                
                relativo_path = os.path.relpath(pasta_raiz, pasta_entrada)
                pasta_destino = os.path.join(pasta_saida, relativo_path)
                
                nome_base = arquivo.replace('.pdf', '').replace('.PDF', '')
                pasta_final = os.path.join(pasta_destino, nome_base)
                
                if not os.path.exists(pasta_final):
                    os.makedirs(pasta_final)
                
                print(f"\n[{total_pdfs}] Convertendo: {arquivo}")
                print(f"    Origem:  {caminho_pdf}")
                print(f"    Destino: {pasta_final}")
                
                try:
                    images = convert_from_path(
                        caminho_pdf,
                        dpi=resolucao_dpi,
                        fmt="png",
                        paths_only=False,
                    )
                    
                    paginas_salvas = 0
                    for i, image in enumerate(images):
                        nome_imagem = f"pagina_{i+1:03d}.png"
                        caminho_imagem = os.path.join(pasta_final, nome_imagem)
                        image.save(caminho_imagem, "PNG")
                        paginas_salvas += 1
                        total_paginas += 1
                    
                    print(f"    ✓ Conversão concluída: {paginas_salvas} páginas")
                    
                except Exception as e:
                    pdfs_com_erro += 1
                    print(f"    ✗ ERRO na conversão: {e}")

    print("\n" + "=" * 60)
    print("RELATÓRIO FINAL")
    print("=" * 60)
    print(f"PDFs processados:    {total_pdfs}")
    print(f"Páginas convertidas: {total_paginas}")
    print(f"PDFs com erro:       {pdfs_com_erro}")
    
    if total_pdfs == 0:
        print("\n⚠  Nenhum arquivo PDF encontrado!")
    elif pdfs_com_erro == 0:
        print("\n🎉 Todas as conversões foram bem-sucedidas!")
    else:
        print(f"\n⚠  {pdfs_com_erro} arquivo(s) tiveram erro na conversão.")

def main():
    if not verificar_pre_requisitos():
        sys.exit(1)
    
    pasta_entrada = "../Passo1_ReunirPDFs"
    pasta_saida = "."
    
    if not os.path.exists(pasta_entrada):
        print(f"❌ Pasta '{pasta_entrada}' não encontrada!")
        sys.exit(1)
    
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)
        print(f"✓ Pasta de saída criada: {pasta_saida}")
    
    print("🚀 Iniciando conversão de PDFs para PNG...")
    print("=" * 60)
    
    converter_pdfs_para_png(pasta_entrada, pasta_saida, resolucao_dpi=300)
    
    print("\n✅ Processamento finalizado!")

if __name__ == "__main__":
    main()