import os

# Obter o caminho absoluto do arquivo excel
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
arquivo_excel = os.path.join(diretorio_atual, 'pontos_turisticos.xlsx')

def run():
    import django
    import wikipediaapi
    import openpyxl
    from app_PP.models import Ponto_Turistico,Endereco_Turistico

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Projeto_PP.settings')
    django.setup()

    def obter_informacoes_wikipedia(nome_ponto_turistico):
        wiki_wiki = wikipediaapi.Wikipedia(
            language='pt',
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent='Wikipedia-API Python/0.5.4'
        )
        page = wiki_wiki.page(nome_ponto_turistico)

        if page.exists():
            informacoes = {
                'pon_nome': nome_ponto_turistico,
                'pon_descricao': page.summary
            }
            
            if 'images' in page.__dict__:
                informacoes['url_imagem'] = page.images[0]
            else:
                informacoes['url_imagem'] = None

            return informacoes
        else:
            return None

    def ler_pontos_turisticos_de_excel(arquivo_excel):
        wb = openpyxl.load_workbook(arquivo_excel)
        planilha = wb.active

        for row in planilha.iter_rows(min_row=2, values_only=True):  # Ignora o cabeçalho (linha 1)
            nome_ponto_turistico = row[0]  # Ajuste para considerar o cabeçalho "Nome do ponto turístico"
            informacoes = obter_informacoes_wikipedia(nome_ponto_turistico)
            if informacoes:
                ponto_turistico = Ponto_Turistico.objects.create(
                    pon_nome=informacoes['pon_nome'],
                    pon_descricao=informacoes['pon_descricao'],
                    pon_latitude=0,
                    pon_longitude=0,
                    pon_status = 0
                )
                ponto_turistico.save()

                novo_Endereco = Endereco_Turistico()

                novo_Endereco.end_pon_id = ponto_turistico
                novo_Endereco.end_cidade = 'N/a'
                novo_Endereco.end_bairro = 'N/a'
                novo_Endereco.end_rua = 'N/a'
                novo_Endereco.end_numero = 0
                
                novo_Endereco.save()
    
    ler_pontos_turisticos_de_excel(arquivo_excel)

    pass

if __name__ == "__main__":
    run()