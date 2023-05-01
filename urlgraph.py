import matplotlib.pyplot as plt

'''
URLGraph is a class that takes in a 2D array of url paths
with a key:value pair showing the most common directories by count.

The build_graph function generates the a bar graph showing the 
occurences of each url path. 

In later versions we might add additional functions or options
to modify the graph output and export options.
'''
class URLGraph:
    def __init__(self, urls, count):
        self.urls = urls
        self.count = count
    
    # URL:{pair[0]} Count: {pair[1]}"
    # Build out our graph from the self.urls and self.count.
    def build_graph(self, options=None):
        # We want to show the (count) amount of URLs
        spacing = (len(self.urls) / self.count) * 2#testing this

        
        # Using a lambda to sort the URLs
        # this should probably be moved to loop_dict or a function elsewhere in the next version
        # as it just prunes the input rather than actually serve a purpose for graph building
        top_urls = sorted(self.urls, key=lambda row: (row[1]), reverse=True)[:self.count]
        print(top_urls)
        

        for index, url in enumerate(top_urls):
            plt.barh(spacing * index, height=1, width=url[1])
            #start_of_text = url[1] + 10 #X-pos of the text, starting at the end of the bar
            start_of_text = 5
            plt.text(start_of_text, spacing * index, str(url[0]), color='black', fontweight='bold', verticalalignment='center', wrap=True)
        
        # Making sure yticks are empty
        plt.yticks([], [])
        # Adding labels
        plt.ylabel('URLs')
        plt.xlabel('Count')
        plt.title(f'Phishing Threats by URL Path')
        plt.get_current_fig_manager().set_window_title('EmThreat')
        #plt.get_current_fig_manager().resize(1500, 600)
        plt.show()