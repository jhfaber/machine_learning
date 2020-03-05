class exploreData():
    def explore(self,df):
        df.head()
        df.shape
        df.info()
        df.describe()
        


class buildChart():
    #COMPARAR X, Y
    import matplotlib.pyplot as plt

    title=''
    label_x=''
    label_y=''

    yticks = [[],[] ] #cambiar nombres de los label en y, [0] originales [1] el reemplazo
    xticks = [[],[]]
    #xticks(tick_val,tick_lab)
    ###########################################
    # COLOR
    #####################################
    # c parameter color receive a dict 


    #################################3
    # ADD TEXT
    ##############################33
    #plt.text(23,3423,'China')


    def __init__(self, title='',label_x='',label_y=''):
        self.title=title
        self.label_x=label_x
        self.label_y=label_y

    # plt.show() #its show plot
    # plt.xscale('log') agrega scala logaritmica
    def hello(self):
        print("ey")

    def labelsAttributes(self):
        plt.xlabel(self.label_x)
        plt.ylabel(self.label_y)
        plt.title(self.title)
    
    def linearChart(self,arr_x,arr_y):
        plt.plot(arr_x,arr_y)
        self.labelsAttributes()


    #Cuando el line plot se satura
    # s scalar array (burbujas)
    def scatterChart(self, arr_x,arr_y,s=None):
        plt.scatter(arr_x,arr_y,s=s)
        self.labelsAttributes()

    #get idea about diistribution
    # bins number of columns
    def histogramChart(self,arr_x, bins=3):
        plt.hist(arr_x, bins=bins)
        self.labelsAttributes()

    def heatmap(self, df):
        #seaborn.heatmap
        #(seaborn.heatmap)
        sns.heatmap(df.corr(), square=True, cmap='RdYlGn')
        pass
