from packages.analyse import ChiSquare, TwinIndex, CheckIC
import plotly
import plotly.graph_objs
import multiprocessing
''' for anaylising a corpus '''

class CorpusAnalysis:
    def __init__(self, txt_files):
        self.twin_data = []
        self.ic_data = []
        self.chi_data = []
        self.colours = ['red', 'blue', 'purple', 'orange', 'black', 'yellow', 'brown', 'green', 'grey', 'pink']

    def run_graphing(self):
        for txt_file in txt_files:
            # print(txt_file)
            with open(txt_file, 'r', encoding='utf-8') as open_txt_file:
                while True:
                    ze_line = open_txt_file.readline()
                    if ze_line.startswith('Title'):
                        title = ze_line.split(':')[1]
                        title = ''.join([x for x in title if x.isalpha() or x.isalpha()])
                        print(title)
                        corpus = open_txt_file.read()
                        colour = self.colours.pop()
                        corpusTwinIndex = CorpusTwinIndex(corpus, title, colour)

                        graph_points = corpusTwinIndex.output_graph()
                        corpusTwinIndex.output_total()
                        self.twin_data.append(graph_points)

                        corpusIC = CorpusIC(corpus, title, colour).output()
                        # multiprocessing.Process(target=CorpusIC().output(), args=(corpus, title, colour, plot_points))
                        self.ic_data.append(corpusIC)

                        corpusCharacterFrequency = CorpusCharacterFrequency(corpus, title, colour).output()
                        self.chi_data.append(corpusCharacterFrequency)
                        break

    def output_twin(self):
        layout = dict(title='Twin Index Vs Character Count',
                      xaxis=dict(title='Character count'),
                      yaxis=dict(title='Twin Index'),
                      )
        fig = dict(data=self.twin_data, layout=layout)
        plotly.offline.plot(fig, filename='twin_index.html')

    def output_ic(self):
        layout = dict(title='Index of Coincidence Vs Character Count',
                      xaxis=dict(title='Character Count'),
                      yaxis=dict(title='Index of Coincidence'),
                      )

        fig = dict(data=self.ic_data, layout=layout)
        plotly.offline.plot(fig, filename='index_f_coincidence.html')

    def output_chi(self):
        layout = dict(title='Chi Square Vs Character Count',
                      xaxis=dict(title='Character Count'),
                      yaxis=dict(title='Chi Square'),
                      )

        fig = dict(data=self.chi_data, layout=layout)
        plotly.offline.plot(fig, filename='chi_square.html')


class CorpusIC:
    def __init__(self, corpus, title, colour):
        self.corpus = corpus
        self.title = title
        self.IC = CheckIC()
        self.plot_points = self.IC.run_normalisation(corpus)
        self.colour = colour

    def output(self):
        plot_points_x, plot_points_y = self.plot_points
        trace = plotly.graph_objs.Scatter(x=plot_points_x,
                                          y=plot_points_y,
                                          name=self.title,
                                          line=dict(
                                              color=self.colour,
                                              width=4
                                          )
                                          )
        return trace


class CorpusCharacterFrequency:
    def __init__(self, corpus, title, colour):
        self.title = title
        self.colour = colour
        self.corpus = corpus
        self.chiSquare = ChiSquare(self.corpus)
        self.plot_points = self.chiSquare.normalisation()

    def output(self):
        plot_points_x, plot_points_y = self.plot_points
        trace = plotly.graph_objs.Scatter(x=plot_points_x,
                                          y=plot_points_y,
                                          name=self.title,
                                          line=dict(
                                              color=self.colour,
                                              width=4
                                          )
                                          )
        return trace



class CorpusTwinIndex:
        def __init__(self, corpus,title, colour):
            self.corpus = corpus
            self.title = title

            self.twinIndex = TwinIndex(self.corpus)

            self.colour = colour

        def output_total(self):
            total =self.twinIndex.run_total()
            print(total)

        def output_graph(self):

            plot_points_x, plot_points_y = self.twinIndex.run_normalisation()

            trace = plotly.graph_objs.Scatter(x=plot_points_x,
                               y=plot_points_y,
                               name=self.title,
                               line=dict(
                                   color=self.colour,
                                   width=4
                               )
            )

            return trace


if __name__ == '__main__':
    txt_files = ['corpus/Alice_in_wonderland.txt',
                 # 'corpus/Pussy_Black-Face_by_Marshall_Saunders.txt',
                 # 'corpus/The_open_sea_by_Edgar_Lee_Masters.txt',
                 # 'corpus/A_Tale_of_Two_Cities_by_Charles_Dickens.txt',
                 # 'corpus/Ulysses_by_James_Joyce.txt',
                 # 'corpus/Heavenly_Gifts_by_Aaron_L_Kolom.txt',
                 # 'corpus/The_Kama_Sutra_of_Vatsyayana_by_Vatsyayana.txt',
                 # 'corpus/The_Adventures_of_Sherlock_Holmes_by_Arthur_Conan_Doyle.txt',
                 # 'corpus/The_Romance_of_Lust_A_Classic_Victorian_erotic_novel_by_Anonymous.txt',
                 # 'corpus/Pride_and_prejeduce.txt',
                 ]
    corpusAnalysis = CorpusAnalysis(txt_files)
    corpusAnalysis.run_graphing()
    # corpusAnalysis.output_chi()
    # corpusAnalysis.output_ic()
    corpusAnalysis.output_twin()

