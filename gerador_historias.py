from textblob import TextBlob
import random
import time
import json
from datetime import datetime
from pathlib import Path

class GeradorHistorias:
    def __init__(self):
        self.idioma = 'pt'
        self.carregar_dados()
        self.historia_atual = []
        self.poder_total = 0
        self.sabedoria_total = 0
        
    def carregar_dados(self):
        """Carrega dados de configuração dos arquivos JSON"""
        try:
            # Carrega dados do idioma
            with open('dados/idiomas.json', 'r', encoding='utf-8') as f:
                self.traducoes = json.load(f)
            
            # Carrega elementos da história
            with open('dados/elementos.json', 'r', encoding='utf-8') as f:
                elementos = json.load(f)
                self.personagens = elementos['personagens']
                self.estados_emocionais = elementos['estados_emocionais']
                self.objetos_magicos = elementos['objetos_magicos']
                self.clima = elementos['clima']
                
        except FileNotFoundError:
            print("Criando arquivos de configuração...")
            self.criar_arquivos_padrao()
            self.carregar_dados()

    def criar_arquivos_padrao(self):
        """Cria arquivos de configuração padrão"""
        Path('dados').mkdir(exist_ok=True)
        
        # Dados de idiomas
        idiomas = {
            'pt': {
                'mensagens': {
                    'bem_vindo': "🌟 Bem-vindo ao Gerador de Histórias Mágicas! 🌟",
                    'tutorial': """
                    📖 COMO JOGAR:
                    1. Uma história inicial será gerada automaticamente
                    2. Você pode continuar a história escrevendo o que acontece depois
                    3. Suas escolhas afetam o poder e a sabedoria do personagem
                    4. Textos positivos aumentam o poder
                    5. Textos longos aumentam a sabedoria
                    6. Digite 'sair' para terminar e salvar sua história
                    7. Digite 'idioma' para trocar entre português e inglês
                    8. Digite 'ajuda' para ver os comandos disponíveis
                    
                    Está pronto para começar sua aventura? (sim/não): """,
                    'comandos': {
                        'sair': 'Sair do jogo',
                        'idioma': 'Mudar idioma',
                        'ajuda': 'Ver comandos',
                        'status': 'Ver status do personagem',
                        'salvar': 'Salvar história atual'
                    },
                    'poder': "⚡ Poder atual: ",
                    'sabedoria': "🎓 Sabedoria atual: ",
                    'continuar': "✍️ Como você quer continuar a história? (ou 'sair' para terminar): ",
                    'analise': "🔮 Análise mágica:",
                    'sentimento': "Sentimento: ",
                    'historia_salva': "📚 História salva em ",
                    'ate_logo': "Até a próxima!"
                }
            },
            'en': {
                'mensagens': {
                    'bem_vindo': "🌟 Welcome to the Magical Story Generator! 🌟",
                    'tutorial': """
                    📖 HOW TO PLAY:
                    1. An initial story will be automatically generated
                    2. You can continue the story by writing what happens next
                    3. Your choices affect the character's power and wisdom
                    4. Positive texts increase power
                    5. Longer texts increase wisdom
                    6. Type 'exit' to end and save your story
                    7. Type 'language' to switch between Portuguese and English
                    8. Type 'help' to see available commands
                    
                    Are you ready to start your adventure? (yes/no): """,
                    'comandos': {
                        'exit': 'Exit game',
                        'language': 'Change language',
                        'help': 'See commands',
                        'status': 'See character status',
                        'save': 'Save current story'
                    },
                    'poder': "⚡ Current power: ",
                    'sabedoria': "🎓 Current wisdom: ",
                    'continuar': "✍️ How do you want to continue the story? (or 'exit' to end): ",
                    'analise': "🔮 Magical analysis:",
                    'sentimento': "Feeling: ",
                    'historia_salva': "📚 Story saved in ",
                    'ate_logo': "See you next time!"
                }
            }
        }

        # Dados dos elementos da história
        elementos = {
            'personagens': {
                'viajante': {'poder': 3, 'sabedoria': 4, 'carisma': 5},
                'mago': {'poder': 7, 'sabedoria': 8, 'carisma': 3},
                'guerreira': {'poder': 8, 'sabedoria': 4, 'carisma': 5},
                'cientista': {'poder': 4, 'sabedoria': 8, 'carisma': 3},
                'artista': {'poder': 2, 'sabedoria': 5, 'carisma': 8}
            },
            'estados_emocionais': {
                'determinado': 'aumentando sua força interior',
                'receoso': 'com as mãos tremendo levemente',
                'curioso': 'com os olhos brilhando de interesse'
            },
            'objetos_magicos': {
                'Cristal do Tempo': 'permite ver fragmentos do futuro',
                'Anel da Verdade': 'revela mentiras e ilusões',
                'Pergaminho Ancestral': 'contém segredos esquecidos'
            },
            'clima': {
                'tempestuoso': 'raios cortavam o céu',
                'nebuloso': 'a névoa densa ocultava os caminhos',
                'estrelado': 'as constelações brilhavam intensamente'
            }
        }

        # Salva os arquivos
        with open('dados/idiomas.json', 'w', encoding='utf-8') as f:
            json.dump(idiomas, f, ensure_ascii=False, indent=4)
            
        with open('dados/elementos.json', 'w', encoding='utf-8') as f:
            json.dump(elementos, f, ensure_ascii=False, indent=4)

    def processar_comando(self, comando):
        """Processa comandos especiais do usuário"""
        comandos = {
            'sair': lambda: self.finalizar_jogo(),
            'exit': lambda: self.finalizar_jogo(),
            'idioma': lambda: self.mudar_idioma(),
            'language': lambda: self.mudar_idioma(),
            'ajuda': lambda: self.mostrar_ajuda(),
            'help': lambda: self.mostrar_ajuda(),
            'status': lambda: self.mostrar_status(),
            'salvar': lambda: self.salvar_historia()
        }
        
        return comandos.get(comando.lower(), lambda: None)()

    def mostrar_ajuda(self):
        """Mostra os comandos disponíveis"""
        if self.idioma == 'pt':
            print("""
╔═══════════════ COMANDOS DISPONÍVEIS ═══════════════╗
║                                                    ║
║  • 'ajuda'    - Mostra esta lista de comandos      ║
║  • 'sair'     - Finaliza e salva a história        ║
║  • 'idioma'   - Troca entre português e inglês     ║
║  • 'status'   - Mostra poder e sabedoria atuais    ║
║                                                    ║
║  Para continuar a história, simplesmente digite    ║
║  o que acontece em seguida!                        ║
╚════════════════════════════════════════════════════╝
        """)
        else:
            print("""
╔═══════════════ AVAILABLE COMMANDS ════════════════╗
║                                                   ║
║  • 'help'     - Shows this command list           ║
║  • 'exit'     - Ends and saves the story          ║
║  • 'language' - Switch between English and PT-BR   ║
║  • 'status'   - Shows current power and wisdom     ║
║                                                   ║
║  To continue the story, simply type what          ║
║  happens next!                                    ║
╚═══════════════════════════════════════════════════╝
        """)

    def mostrar_status(self):
        """Mostra status atual do personagem"""
        print(f"\n📊 Status do Personagem:")
        print(f"⚡ Poder: {self.poder_total}")
        print(f"🎓 Sabedoria: {self.sabedoria_total}")
        return True

    def finalizar_jogo(self):
        """Finaliza o jogo salvando a história"""
        self.salvar_historia()
        return False

    def gerar_historia_base(self):
        """Gera a história inicial baseada no idioma selecionado"""
        # Definição dos elementos e seus atributos
        elementos = {
            'pt': {
                'personagens': {
                    'viajante': {'poder': 3, 'sabedoria': 4, 'carisma': 5},
                    'mago': {'poder': 7, 'sabedoria': 8, 'carisma': 3},
                    'guerreira': {'poder': 8, 'sabedoria': 4, 'carisma': 5},
                    'cientista': {'poder': 4, 'sabedoria': 8, 'carisma': 3},
                    'artista': {'poder': 2, 'sabedoria': 5, 'carisma': 8}
                },
                'locais': ['floresta mágica', 'cidade futurista', 'montanha antiga', 'laboratório secreto'],
                'eventos': ['descobriu um portal misterioso', 'encontrou um artefato antigo', 
                           'resolveu um enigma complexo', 'fez uma descoberta revolucionária']
            },
            'en': {
                'personagens': {
                    'traveler': {'poder': 3, 'sabedoria': 4, 'carisma': 5},
                    'wizard': {'poder': 7, 'sabedoria': 8, 'carisma': 3},
                    'warrior': {'poder': 8, 'sabedoria': 4, 'carisma': 5},
                    'scientist': {'poder': 4, 'sabedoria': 8, 'carisma': 3},
                    'artist': {'poder': 2, 'sabedoria': 5, 'carisma': 8}
                },
                'locais': ['magical forest', 'futuristic city', 'ancient mountain', 'secret laboratory'],
                'eventos': ['discovered a mysterious portal', 'found an ancient artifact', 
                           'solved a complex riddle', 'made a revolutionary discovery']
            }
        }
        
        # Seleciona elementos baseados no idioma atual
        personagem_nome = random.choice(list(elementos[self.idioma]['personagens'].keys()))
        local = random.choice(elementos[self.idioma]['locais'])
        evento = random.choice(elementos[self.idioma]['eventos'])
        
        # Define os atributos iniciais do personagem
        self.poder_total = elementos[self.idioma]['personagens'][personagem_nome]['poder']
        self.sabedoria_total = elementos[self.idioma]['personagens'][personagem_nome]['sabedoria']
        
        # Constrói a história no idioma correto
        if self.idioma == 'pt':
            historia = f"Um(a) {personagem_nome} na {local} {evento}."
        else:
            # Ajusta artigos e estrutura para inglês
            artigo = 'an' if personagem_nome[0].lower() in 'aeiou' else 'a'
            historia = f"{artigo.capitalize()} {personagem_nome} in the {local} {evento}."
        
        # Adiciona a história inicial ao histórico
        self.historia_atual.append({
            'texto': historia,
            'timestamp': datetime.now(),
            'poder': self.poder_total,
            'sabedoria': self.sabedoria_total
        })
        
        return historia

    def analisar_sentimento_e_poder(self, texto):
        """Analisa o sentimento do texto e calcula as alterações de poder e sabedoria"""
        analise = TextBlob(texto)
        
        # Análise de sentimento (-1 a 1)
        sentimento = analise.sentiment.polarity
        
        # Palavras positivas e negativas em português e inglês
        palavras_positivas = {
            'pt': ['feliz', 'alegre', 'amor', 'vitória', 'sucesso', 'força', 'coragem', 
                   'esperança', 'triunfo', 'magia', 'brilhante', 'poderoso'],
            'en': ['happy', 'joy', 'love', 'victory', 'success', 'strength', 'courage',
                   'hope', 'triumph', 'magic', 'bright', 'powerful']
        }
        
        palavras_negativas = {
            'pt': ['triste', 'medo', 'fracasso', 'derrota', 'morte', 'dor', 'escuridão',
                   'perigo', 'fraco', 'perdido'],
            'en': ['sad', 'fear', 'failure', 'defeat', 'death', 'pain', 'darkness',
                   'danger', 'weak', 'lost']
        }
        
        # Contagem de palavras especiais
        palavras = texto.lower().split()
        palavras_pos = sum(1 for p in palavras if p in palavras_positivas[self.idioma])
        palavras_neg = sum(1 for p in palavras if p in palavras_negativas[self.idioma])
        
        # Cálculo do poder baseado em sentimentos
        poder_ganho = 0
        if sentimento > 0:
            poder_ganho = 2 + palavras_pos
        elif sentimento < 0:
            poder_ganho = -1 - palavras_neg
        
        # Cálculo da sabedoria baseado no comprimento e complexidade
        sabedoria_ganha = len(texto.split()) // 10  # 1 ponto a cada 10 palavras
        
        # Atualização dos totais
        self.poder_total = max(0, self.poder_total + poder_ganho)
        self.sabedoria_total += sabedoria_ganha
        
        # Preparar mensagem de feedback
        if self.idioma == 'pt':
            feedback = {
                'sentimento': 'positivo' if sentimento > 0 else 'negativo' if sentimento < 0 else 'neutro',
                'poder_ganho': poder_ganho,
                'sabedoria_ganha': sabedoria_ganha,
                'analise_detalhada': f"""
📊 Análise Detalhada:
• Sentimento: {sentimento:.2f} (-1 a +1)
• Palavras positivas encontradas: {palavras_pos}
• Palavras negativas encontradas: {palavras_neg}
• Poder ganho/perdido: {poder_ganho:+d}
• Sabedoria ganha: +{sabedoria_ganha}
"""
            }
        else:
            feedback = {
                'sentimento': 'positive' if sentimento > 0 else 'negative' if sentimento < 0 else 'neutral',
                'poder_ganho': poder_ganho,
                'sabedoria_ganha': sabedoria_ganha,
                'analise_detalhada': f"""
📊 Detailed Analysis:
• Sentiment: {sentimento:.2f} (-1 to +1)
• Positive words found: {palavras_pos}
• Negative words found: {palavras_neg}
• Power gained/lost: {poder_ganho:+d}
• Wisdom gained: +{sabedoria_ganha}
"""
            }
        
        return feedback

    def mudar_idioma(self):
        """Permite ao usuário trocar o idioma durante o jogo"""
        print("""
╔════════════════════════════════════════╗
║    Selecione seu idioma                ║
║    Select your language                ║
║                                        ║
║    1. Português (BR)                   ║
║    2. English                          ║
╚════════════════════════════════════════╝
    """)
        
        while True:
            escolha = input("Digite 1 ou 2 / Enter 1 or 2: ").strip()
            if escolha == "1":
                self.idioma = 'pt'
                return "🌟 Idioma alterado para Português! 🌟"
            elif escolha == "2":
                self.idioma = 'en'
                return "🌟 Language changed to English! 🌟"
            print("Opção inválida / Invalid option")

    def selecionar_idioma_inicial(self):
        """Permite ao usuário selecionar o idioma inicial"""
        print("""
╔════════════════════════════════════════╗
║    Selecione seu idioma preferido      ║
║    Select your preferred language       ║
║                                        ║
║    1. Português (BR)                   ║
║    2. English                          ║
╚════════════════════════════════════════╝
        """)
        
        while True:
            escolha = input("Digite 1 ou 2 / Enter 1 or 2: ").strip()
            if escolha == "1":
                self.idioma = 'pt'
                break
            elif escolha == "2":
                self.idioma = 'en'
                break
            print("Opção inválida / Invalid option")

    def explicar_sistema(self):
        """Explica o sistema de poder e sabedoria com exemplos"""
        if self.idioma == 'pt':
            print("""
╔═══════════════════════ SISTEMA DE JOGO ══════════════════════╗
║                                                              ║
║  PODER (⚡)                                                  ║
║  • Base do sistema:                                         ║
║    - Texto positivo: +2 pontos de poder                     ║
║    - Texto negativo: -1 ponto de poder                      ║
║                                                              ║
║  • Palavras especiais:                                      ║
║    Positivas (+1 cada): feliz, amor, vitória, coragem       ║
║    Negativas (-1 cada): triste, medo, derrota, dor          ║
║                                                              ║
║  • Exemplo positivo:                                        ║
║    "O guerreiro corajoso venceu com amor"                   ║
║    → +2 (base) +2 (palavras: corajoso, amor) = +4 poder    ║
║                                                              ║
║  • Exemplo negativo:                                        ║
║    "O guerreiro sentiu medo e tristeza"                     ║
║    → -1 (base) -2 (palavras: medo, tristeza) = -3 poder    ║
║                                                              ║
║  SABEDORIA (🎓)                                             ║
║  • Ganha 1 ponto a cada 10 palavras escritas                ║
║  • Exemplo:                                                  ║
║    "O guerreiro corajoso enfrentou o dragão com força"      ║
║    → 8 palavras = 0 pontos de sabedoria                     ║
║    "O guerreiro corajoso enfrentou o dragão com força       ║
║     e descobriu um antigo segredo mágico na caverna"        ║
║    → 15 palavras = 1 ponto de sabedoria                     ║
║                                                              ║
║  DICAS IMPORTANTES:                                         ║
║  1. Combine emoções positivas com textos longos             ║
║  2. Evite repetir as mesmas palavras                        ║
║  3. Desenvolva a história com detalhes                      ║
║  4. O poder nunca fica negativo                             ║
║  5. A sabedoria sempre aumenta                              ║
╚══════════════════════════════════════════════════════════════╝
        """)
        else:
            print("""
╔═══════════════════════ GAME SYSTEM ═══════════════════════╗
║                                                           ║
║  POWER (⚡)                                               ║
║  • Base system:                                          ║
║    - Positive text: +2 power points                      ║
║    - Negative text: -1 power point                       ║
║                                                           ║
║  • Special words:                                        ║
║    Positive (+1 each): happy, love, victory, courage     ║
║    Negative (-1 each): sad, fear, defeat, pain          ║
║                                                           ║
║  • Positive example:                                     ║
║    "The brave warrior won with love"                     ║
║    → +2 (base) +2 (words: brave, love) = +4 power       ║
║                                                           ║
║  • Negative example:                                     ║
║    "The warrior felt fear and sadness"                   ║
║    → -1 (base) -2 (words: fear, sadness) = -3 power     ║
║                                                           ║
║  WISDOM (🎓)                                             ║
║  • Gains 1 point for every 10 words written              ║
║  • Example:                                              ║
║    "The brave warrior faced the dragon with strength"    ║
║    → 8 words = 0 wisdom points                          ║
║    "The brave warrior faced the dragon with strength     ║
║     and discovered an ancient magical secret in cave"    ║
║    → 15 words = 1 wisdom point                          ║
║                                                           ║
║  IMPORTANT TIPS:                                         ║
║  1. Combine positive emotions with long texts            ║
║  2. Avoid repeating the same words                       ║
║  3. Develop the story with details                       ║
║  4. Power never goes negative                            ║
║  5. Wisdom always increases                              ║
╚═══════════════════════════════════════════════════════════╝
        """)
        
        # Aguardar o usuário ler
        input("\nPressione ENTER para continuar..." if self.idioma == 'pt' else "\nPress ENTER to continue...")

    def interagir(self):
        """Método principal de interação"""
        # Seleção inicial de idioma
        self.selecionar_idioma_inicial()
        
        # Boas-vindas e explicação do sistema
        print("\n" + self.traducoes[self.idioma]['mensagens']['bem_vindo'])
        self.explicar_sistema()
        
        # Tutorial e início do jogo
        resposta = input(self.traducoes[self.idioma]['mensagens']['tutorial']).lower()
        
        if resposta not in ['sim', 'yes', 's', 'y']:
            # Mensagem de despedida traduzida
            print("See you next time!" if self.idioma == 'en' else "Até a próxima!")
            return

        # Iniciar a história
        historia = self.gerar_historia_base()
        historia_inicial_msg = "📖 Initial story:" if self.idioma == 'en' else "📖 História inicial:"
        print(f"\n{historia_inicial_msg}", historia)
        jogando = True
        
        while jogando:
            try:
                # Mostrar status atual com mensagens traduzidas
                if self.idioma == 'en':
                    print(f"\n⚡ Current Power: {self.poder_total}")
                    print(f"🎓 Current Wisdom: {self.sabedoria_total}")
                else:
                    print(f"\n⚡ Poder atual: {self.poder_total}")
                    print(f"🎓 Sabedoria atual: {self.sabedoria_total}")
                
                # Menu de comandos disponíveis
                print("\n📜 Comandos / Commands:")
                print("• 'ajuda'/'help' - Ver todos os comandos / See all commands")
                print("• 'sair'/'exit' - Finalizar história / End story")
                print("• 'idioma'/'language' - Trocar idioma / Change language")
                
                # Entrada do usuário traduzida
                prompt = "✍️ What happens next? " if self.idioma == 'en' else "✍️ O que acontece depois? "
                continuacao = input(f"\n{prompt}").lower()
                
                # Verificar comandos
                if continuacao in ['sair', 'exit']:
                    self.salvar_historia()
                    # Mensagem de despedida traduzida
                    print("See you next time!" if self.idioma == 'en' else "Até a próxima!")
                    jogando = False
                    break
                    
                if continuacao in ['idioma', 'language']:
                    print(self.mudar_idioma())
                    continue
                    
                if continuacao in ['ajuda', 'help']:
                    self.mostrar_ajuda()
                    continue
                    
                if continuacao in ['status']:
                    self.mostrar_status()
                    continue
                
                # Processar a continuação da história
                if continuacao.strip():
                    analise = self.analisar_sentimento_e_poder(continuacao)
                    analise_msg = "🔮 Magical Analysis:" if self.idioma == 'en' else "🔮 Análise mágica:"
                    print(f"\n{analise_msg}")
                    print(analise['analise_detalhada'])
                    
                    self.historia_atual.append({
                        'texto': continuacao,
                        'timestamp': datetime.now(),
                        'poder': self.poder_total,
                        'sabedoria': self.sabedoria_total
                    })
                
            except Exception as e:
                erro_msg = "Error: " if self.idioma == 'en' else "Erro: "
                print(f"{erro_msg}{e}")
                continuar_msg = "Continue? (yes/no): " if self.idioma == 'en' else "Continuar? (sim/não): "
                resposta = input(continuar_msg).lower()
                if resposta not in ['sim', 'yes', 's', 'y']:
                    jogando = False
                    break

    def salvar_historia(self):
        """Salva a história em um arquivo"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"historia_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("🌟 " + (
                    "HISTÓRIA MÁGICA" if self.idioma == 'pt' else 
                    "MAGICAL STORY"
                ) + " 🌟\n\n")
                
                for parte in self.historia_atual:
                    f.write(f"{parte['texto']}\n")
                    f.write(f"[Poder: {parte['poder']} | Sabedoria: {parte['sabedoria']}]\n\n")
            
            mensagem = (
                f"📚 História salva em {filename}" if self.idioma == 'pt' 
                else f"📚 Story saved in {filename}"
            )
            print(mensagem)
            
        except Exception as e:
            mensagem_erro = (
                f"Erro ao salvar história: {str(e)}" if self.idioma == 'pt'
                else f"Error saving story: {str(e)}"
            )
            print(mensagem_erro)

if __name__ == "__main__":
    gerador = GeradorHistorias()
    gerador.interagir() 