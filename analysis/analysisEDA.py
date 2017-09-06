import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import sqlite3 as sqlite
import pandas as pd
from scipy import stats
import pylab
from sklearn.neighbors import KernelDensity
from scipy.stats import mode
import json
from json2html import *

def ImportData():
  conn = sqlite.connect("/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/data/yelpCleanDB.sqlite")
  data = pd.read_sql_query("SELECT * FROM DataCompetitionCityAdded", conn)
  # for index, row in data.iterrows():
  #   if row['city'] == 'San Francisco - Downtown' or row['city'] == 'San Francisco - Outer':
  #     # print(row)
  #     del row
  print(len(data))
  data = data[data['category'] != 'food']
  data = data[data['category'] != 'nightlife']
  data = data[data['city'] != 'San Francisco - Downtown']
  data = data[data['city'] != 'San Francisco - Outer']
  print(len(data))
  return data

def Stats(data):
  pd.options.display.float_format = '{:,.2f}'.format #display a pandas dataframe with a given format

  data = data[['rating', 'review_count', 'category', 'query_price',
               'closest2Distance','closest2Price', 'closest2Rating',
               'closest5Distance', 'closest5Price','closest5Rating',
               'closest10Distance', 'closest10Price','closest10Rating',
               'closest15Distance', 'closest15Price','closest15Rating']]

  # data.columns =
  dataByCategory = data.groupby('category')

  dataPivotTable = pd.DataFrame(columns=['category', 'variable', 'Stats', 'value'])
  categories = ['bars', 'beautysvc', 'coffee', 'giftshops', 'restaurants'] #data index
  variables= ['closest10Distance', 'closest10Price', 'closest10Rating', 'closest15Distance',
    'closest15Price', 'closest15Rating', 'closest2Distance', 'closest2Price', 'closest2Rating',
    'closest5Distance', 'closest5Price', 'closest5Rating', 'query_price', 'rating', 'review_count'] #labels
  columns = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
  stats = pd.DataFrame(dataByCategory.describe())
  for category in categories:
    for variable in variables:
      for i in range(len(columns)):
        value = stats.loc[category][variable][i]
        dataPivotTable.loc[len(dataPivotTable)] = [category, variable, columns[i], value]

  statsTable = pd.pivot_table(dataPivotTable, values='value', index=['category', 'variable'], columns=['Stats'])

  statsTable.index.names = ['Category', 'Variables']
  # category:
  levels0 = ['Bars', 'Beauty and Spas', 'Coffee and Tea', 'Giftshops', 'Restaurants']
  # print(statsTable.index.levels[0])
  # variables:
  levels1 = ['Distance of Closest 10 Competitors', 'Price of Closest 10 Competitors', 'Rating of Closest 10 Competitors',
       'Distance of Closest 15 Competitors', 'Price of Closest 15 Competitors', 'Rating of Closest 15 Competitors',
       'Distance of Closest 2 Competitors', 'Price of Closest 2 Competitors', 'Rating of Closest 2 Competitors',
       'Distance of Closest 5 Competitors', 'Price of Closest 5 Competitors', 'Rating of Closest 5 Competitors', 'Price',
       'Rating', 'Review Count']
  # print(statsTable.index.levels[1])

  statsTable.index.set_levels(levels0, level=0, inplace=True)
  statsTable.index.set_levels(levels1, level=1, inplace=True)
  statsTable.to_csv('/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/yelp/static/plots/statsTable.csv')
  return statsTable


def CategoryHeatmaps(data):
  dataAxes1 = data.pivot_table(values='query_price', index='rating', columns='category') #VERY GOOD
  dataAxes2 = data.pivot_table(values='rating', index='query_price', columns='category') #VERY GOOD

  # fig1 = plt.figure(figsize=(10,10))
  fig1, axes = plt.subplots(nrows=2, ncols=1, figsize=(10,10), dpi = 100)
  fig1.suptitle('Price-Rating Relationship Across Categories', fontsize=14)
  plt.subplot(2, 1, 1)
  axes = sns.heatmap(dataAxes1.dropna(), cmap='coolwarm', linecolor='white', linewidths=1, annot=True, #vmax=4, vmin=0,
    xticklabels=['Bars', 'Beauty & Spas', 'Coffee & Tea', 'Giftshops', 'Restaurants'],
    cbar_kws={'label': ''},
    annot_kws={'fontsize': 10})
  # axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
  axes.set_ylabel('Ratings', rotation=0)
  axes.yaxis.set_label_coords(-0.05 ,1.02)
  axes.set_xlabel('')
  # axes.collections[0].colorbar.set_label("Hello", rotation=0)
  axes.set_title('Colormap: Price Levels', fontsize=12)

  # Only y-axis labels need their rotation set, x-axis labels already have a rotation of 0
  _, labels = plt.yticks()
  plt.setp(labels, rotation=0)
  # _, labels = plt.xticks()
  # plt.setp(labels, rotation=0)

  # fig2 = plt[0].figure(figsize=(10,10))
  plt.subplot(2, 1, 2)
  axes = sns.heatmap(dataAxes2.dropna(), cmap='coolwarm', linecolor='white', linewidths=1, annot=True, #vmax=5, vmin=0,
    xticklabels=['Bars', 'Beauty & Spas', 'Coffee & Tea', 'Giftshops', 'Restaurants'],
    cbar_kws={'label': ''},
    annot_kws={'fontsize': 10})
  # axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
  axes.set_ylabel('Price Levels', rotation=0)
  axes.yaxis.set_label_coords(-0.05 ,1.02)
  axes.set_xlabel('')
  axes.set_title('Colormap: Ratings', fontsize=12)

  # Only y-axis labels need their rotation set, x-axis labels already have a rotation of 0
  _, labels = plt.yticks()
  plt.setp(labels, rotation=0)
  # _, labels = plt.xticks()
  # plt.setp(labels, rotation=0)
  plt.savefig('/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/yelp/static/plots/categoryheatmaps.png', dpi=200)
  plt.show()


def Histograms(data):
  # fig3 = plt.figure(figsize=(10,10))
  def kde_sklearn(x, x_grid, bandwidth=0.2, **kwargs):
    """Kernel Density Estimation with Scikit-learn"""
    kde_skl = KernelDensity(bandwidth=bandwidth, **kwargs, kernel='gaussian')
    kde_skl.fit(x[:, np.newaxis])
    # score_samples() returns the log-likelihood of the samples
    log_pdf = kde_skl.score_samples(x_grid[:, np.newaxis])
    return np.exp(log_pdf)

  plt.style.use('seaborn-deep') #bmh

  categories = data['category'].unique()

  dataRestaurants = data[data['category'] == 'restaurants']
  dataBars = data[data['category'] == 'bars']
  dataCoffee = data[data['category'] == 'coffee']
  dataBeauty = data[data['category'] == 'beautysvc']
  dataGiftshop = data[data['category'] == 'giftshops']

  dataPriceByCategory = [dataRestaurants['query_price'], dataBars['query_price'],
    dataCoffee['query_price'], dataBeauty['query_price'], dataGiftshop['query_price']]
  dataRatingByCategory = [dataRestaurants['rating'], dataBars['rating'],
    dataCoffee['rating'], dataBeauty['rating'], dataGiftshop['rating']]

  dataPriceByCategoryDF = pd.DataFrame(columns = ['Restaurants','Bars','Coffee','Giftshops','Beauty'])
  dataPriceByCategoryDF['Restaurants'] = dataRestaurants['query_price']
  dataPriceByCategoryDF['Bars'] = dataBars['query_price']
  dataPriceByCategoryDF['Coffee'] = dataCoffee['query_price']
  dataPriceByCategoryDF['Giftshops'] = dataGiftshop['query_price']
  dataPriceByCategoryDF['Beauty'] = dataBeauty['query_price']
  # print(dataRestaurants['query_price'])
  # print(dataPriceByCategoryDF.head())

  fig4 = plt.figure(figsize=(10,10))
  binsPrice = np.linspace(1, 4, num= 5)
  binsRating = np.linspace(1, 5, num = 10)
  x_gridPrice = np.linspace(0, 5, 100)
  x_gridRating = np.linspace(0, 6, 100)
  plt.subplot(2, 2, 1)
  plt.hist(dataPriceByCategory, alpha=0.7, bins=binsPrice,
    label=['Restaurants', 'Bars', 'Coffee & Tea', 'Beauty & Spas', 'Giftshops'], histtype = "bar")
  plt.title('Price by Category')
  plt.legend(loc='upper right')


  plt.subplot(2, 2, 2)
  plt.plot(x_gridPrice, kde_sklearn(data['query_price'], x_gridPrice, bandwidth=0.4),
               label='KDE', linewidth=3, alpha=0.5)
  plt.hist(data['query_price'], bins=4, fc='gray', histtype='stepfilled', alpha=0.3, normed=True, label=None)
  plt.title('Price All Categories')
  # labels = [1,2,3,4]
  # plt.set_xticklabels(['$%.lf$' % x for x in labels])
  mean = data['query_price'].mean()
  median = data['query_price'].median()
  (_, idx, counts) = np.unique(data['query_price'], return_index=True, return_counts=True)
  index = idx[np.argmax(counts)]
  mode = data['query_price'].iloc[index]
  plt.axvline(mean, label='Mean:{:2.1f}'.format(mean), color='b', linestyle='-', linewidth=1) #label='Mean:{:2.1f}'.format(mean)
  plt.axvline(median, label='Median:{:2.1f}'.format(median), color='r', linestyle='--', linewidth=1) #label='Median:{:2.1f}'.format(median)
  # print(modeSkewness, medianSkewness)
  # ax[row, col].text(.5,1.3, title, weight='heavy', horizontalalignment='center', fontsize=13, transform=ax[row, col].transAxes)
  plt.axvline(mode, label='Mode:{:2.1f}'.format(mode), color='g', linestyle='-.', linewidth=1) #label='Mode:{:2.1f}'.format(mode)
  plt.legend(loc='upper right')


  plt.subplot(2, 2, 3)
  plt.hist(dataRatingByCategory, alpha=0.7, bins=binsRating,
    label=['Restaurants', 'Bars',  'Coffee & Tea', 'Beauty & Spas', 'Giftshops'], histtype = "bar")
  plt.title('Rating by Category')
  plt.legend(loc='upper left')

  plt.subplot(2, 2, 4)
  plt.plot(x_gridRating, kde_sklearn(data['rating'], x_gridRating, bandwidth=0.4),
               label='KDE', linewidth=3, alpha=0.5)
  plt.hist(data['rating'], bins=4, fc='gray', histtype='stepfilled', alpha=0.3, normed=True, label=None)
  plt.title('Rating All Categories')
  # labels = [1,2,3,4,5]
  # plt.set_xticklabels(['$%.lf$' % x for x in labels])
  mean = data['rating'].mean()
  median = data['rating'].median()
  (_, idx, counts) = np.unique(data['rating'], return_index=True, return_counts=True)
  index = idx[np.argmax(counts)]
  mode = data['rating'].iloc[index]
  plt.axvline(mean, label='Mean:{:2.1f}'.format(mean), color='b', linestyle='-', linewidth=1) #label='Mean:{:2.1f}'.format(mean)
  plt.axvline(median, label='Median:{:2.1f}'.format(median), color='r', linestyle='--', linewidth=1) #label='Median:{:2.1f}'.format(median)
  # print(modeSkewness, medianSkewness)
  # ax[row, col].text(.5,1.3, title, weight='heavy', horizontalalignment='center', fontsize=13, transform=ax[row, col].transAxes)
  plt.axvline(mode, label='Mode:{:2.1f}'.format(mode), color='g', linestyle='-.', linewidth=1) #label='Mode:{:2.1f}'.format(mode)
  plt.legend(loc='upper left')

  plt.savefig('/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/yelp/static/plots/histogramsByCategory.png', dpi=200)
  # plt.hist(data['rating'], alpha=0.7, bins=binsRating, histtype = "bar")
  # plt.title('Rating All Categories')

  # kde = stats.gaussian_kde(x)
  # xx = np.linspace(0, 9, 1000)
  # plt, ax = plt.subplots(figsize=(8,6))
  # ax.hist(x, normed=True, bins=bins, alpha=0.3)
  # ax.plot(xx, kde(xx))


  cols = [0,0,1,1,2,2]
  rows = [0,1,0,1,0,1]
  title = ['Restaurants', 'Bars', 'Coffee & Tea', 'Beauty & Spas', 'Giftshops', 'All Categories']
  priceLabels = ['$', '$$', '$$$', '$$$$']
  categories = [dataRestaurants, dataBars, dataCoffee, dataBeauty, dataGiftshop, data]
  # fig = plt.figure(figsize=(8,4))
  fig4, axes = plt.subplots(nrows=2, ncols=3,figsize=(10,10), dpi = 100)
  fig4.suptitle('Price Histograms', fontsize=14)
  # for category, row, col, ax in zip(categories, rows, cols, axes):
  for i, row, col in zip(range(len(categories)), rows, cols):
    print(i, row, col)
    axes[row, col].hist(categories[i]['query_price'], histtype='stepfilled', alpha=0.5, bins=[0.5,1,2,3,4,5])
    # axes[row, col].set_xlabel(priceLabels)
    # axes[row, col].set_xticks([1, 2, 3, 4])
    x = range(1, 5)
    axes[row, col].set_xticks(x)
    labels = ['$', '$$', '$$$', '$$$$']
    labels = [1,2,3,4]
    axes[row, col].set_xticklabels(['$%.lf$' % y for y in labels])
    # axes[row, col].set_xticklabels('$, $$, $$$, $$$$', fontsize=12)
    axes[row, col].set_title(title[i])
  fig4.savefig('/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/yelp/static/plots/priceHistograms.png', dpi=200)

  fig5, axes = plt.subplots(nrows=2, ncols=3,figsize=(10,10), dpi = 100)
  fig5.suptitle('Rating Histograms', fontsize=14)
  # for category, row, col, ax in zip(categories, rows, cols, axes):
  for i, row, col in zip(range(len(categories)), rows, cols):
    print(i, row, col)
    axes[row, col].hist(categories[i]['rating'], histtype='stepfilled', alpha=0.5, bins=[0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5])
    # axes[row, col].set_xlabel(priceLabels)
    # axes[row, col].set_xticks([1, 2, 3, 4])
    x = range(1, 6)
    axes[row, col].set_xticks(x)
    labels = [1,2,3,4,5]
    axes[row, col].set_xticklabels(['$%.lf$' % y for y in labels])
    # axes[row, col].set_xticklabels('$, $$, $$$, $$$$', fontsize=12)
    axes[row, col].set_title(title[i])

  fig5.savefig('/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/yelp/static/plots/ratingHistograms.png', dpi=200)

  plt.show()


def JointPlots(data):
  categories = ['restaurants', 'bars', 'coffee', 'beautysvc', 'giftshops']

  dataRestaurants = data[data['category'] == 'restaurants']
  dataBars = data[data['category'] == 'bars']
  dataCoffee = data[data['category'] == 'coffee']
  dataBeauty = data[data['category'] == 'beautysvc']
  dataGiftshop = data[data['category'] == 'giftshops']

  rows = [0,1,0,1,0,1]
  cols = [0,0,1,1,2,2]
  title = ['Restaurants', 'Bars', 'Coffee & Tea', 'Beauty & Spas', 'Giftshops', 'All Categories']

  fig6, axes = plt.subplots(nrows=2, ncols=3, figsize=(10,10), dpi = 100)
  fig6.suptitle('Price-Rating Relationship Across Categories', fontsize=14)
  for i, row, col, t in zip(categories, rows, cols, title):
    print(i, row, col)
    g = sns.jointplot(x='query_price',y='rating', data=data[data['category'] == i], kind='kde',
      marginal_kws=dict(bw=1),  #, ax=axes[row, col]
      annot_kws=dict(stat="pearsonr"),
      edgecolor="w", linewidth=1, ax=axes[row, col])
    g.plot_joint(sns.kdeplot, zorder=3, n_levels=5) #ax=axes[row, col]
    axes[row, col].set_title(t, fontsize=10)

    dataPearson = data[data['category'] == i]
    x = dataPearson['query_price']
    y = dataPearson['rating']
    pearsonr = stats.pearsonr(x, y)
    axes[row, col].set_xlabel('Pearsonr:{:2.3f}  p-value:{:2.2f}'.format(pearsonr[0], pearsonr[1]))
    axes[row, col].xaxis.set_label_coords(0.5,0.10)
    # axes[row, col].set_ylabel("Rating")
    # axes[row, col].xaxis.labelpad = 5
    # axes[row, col].yaxis.labelpad = 5

  k = sns.jointplot(x='query_price',y='rating', data=data, kind='kde',
      marginal_kws=dict(bw=1),
      annot_kws=dict(stat="pearsonr"),
      edgecolor="w", linewidth=1, ax=axes[1, 2])
  k.plot_joint(sns.kdeplot, zorder=3, n_levels=5)
  axes[1, 2].set_title(title[5], fontsize=10)
  pearsonr = stats.pearsonr(data['rating'], data['query_price'])
  axes[1, 2].set_xlabel('Pearsonr:{:2.3f}  p-value:{:2.2f}'.format(pearsonr[0], pearsonr[1]))
  axes[1, 2].xaxis.set_label_coords(0.5,0.10)

  fig6.text(0.5, 0.04, 'Price Levels (1:Low; 4:High)', ha='center', fontsize=12)
  fig6.text(0.04, 0.5, 'Ratings', va='center', rotation='vertical', fontsize=12)

  fig6.savefig('/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/yelp/static/plots/jointplots.png', dpi=200)
  plt.show()


def Correlations(data): #only for pooled data
  fig7, axes = plt.subplots(nrows=3, ncols=2, figsize=(10,10), dpi = 100)
  dataCorrCity = data[['numberOfCompetitorsCity', 'avgPriceCity', 'avgRatingCity', 'population', 'area']].drop_duplicates()
  dataCorrCompClosest2 = data[['closest2Distance', 'closest2Rating', 'closest2Price']]
  dataCorr = data[['rating', 'query_price', 'review_count']]
  dataCorrZipcode = data[['numberOfCompetitorsZipcode', 'avgPriceZipcode', 'avgRatingZipcode', 'population', 'area']].drop_duplicates()
  dataCorrCompDistance = data[['closest2Distance', 'closest5Distance', 'closest10Distance', 'closest15Distance']]
  dataCorrFinal = data[['rating', 'query_price', 'review_count', 'closest2Distance', 'closest2Rating', 'closest2Price']]

  datasets = [dataCorrCity, dataCorrCompClosest2, dataCorr,
    dataCorrZipcode, dataCorrCompDistance, dataCorrFinal]
  rows = [0,1,2,0,1,2] #from left to right= 1-4-5-2-3-6
  cols = [0,1,0,1,0,1]
  titles = ['Competition & City Variables',
    'Closest 2 Competitors',
    'Business Variables',
    'Competition & Zipcode Variables',
    'Distance Variables',
    'Business & Competition Variables']

  xLabels = [['Competitors', 'Comp.Price', 'Comp.Rating', 'Population', ''],
    ['Dist.2', 'Comp.Rating', ''],
    ['Rating', 'Price', ''],
    ['Competitors', 'Comp.Price', 'Comp.Rating', 'Population', ''],
    ['Distance-2', 'Distance-5', 'Distance-10', ''],
    ['Rating', 'Price', 'Review', 'Comp.Dist.', 'Comp.Rating', '']]

  yLabels = [['', ' Price', 'Rating', 'Population', 'Area'],
    ['', 'Comp.Rating', 'Comp.Price'],
    ['', 'Price', 'Review'],
    ['', 'Price', 'Rating', 'Population', 'Area'],
    ['', 'Distance-5', 'Distance-10', 'Distance-15'],
    ['', 'Price', 'Review', 'Dist.2', 'Comp.Rating', 'Comp.Price']]

  fig7.suptitle('Correlations Among Variables', fontsize=14)
  # for category, row, col, ax in zip(categories, rows, cols, axes):
  for dataset, row, col, title, xLabel, yLabel in zip(datasets, rows, cols, titles, xLabels, yLabels):
    corr = dataset.corr() # np.corrcoef
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
      c = sns.heatmap(corr, mask=mask, vmax=1, vmin=-0.3, square=True, cbar_kws={"pad": 0.01, 'shrink': 0.7, 'fraction': 0.10}, ax=axes[row, col]) #annot=True, annot_kws : dict of key, value mappings, optional Keyword arguments for ax.text when annot is True.
      axes[row, col].text(.5,.85, title, horizontalalignment='center', transform=axes[row, col].transAxes)
      axes[row, col].set_xticklabels(xLabel, rotation=25, fontsize=8)
      axes[row, col].xaxis.set_ticks_position('none')
      axes[row, col].set_yticklabels(yLabel, rotation='horizontal', fontsize=8)
      axes[row, col].yaxis.set_ticks_position('none')
      # axes[row, col].set_xlabel("Price")
    # axes[row, col].set_ylabel("Rating")
    # axes[row, col].xaxis.labelpad = 5
    # axes[row, col].yaxis.labelpad = 5

    # axes[row, col].hist(categories[i]['query_price'], bins=[0.5,1,2,3,4,5])
    # # axes[row, col].set_xlabel(priceLabels)
    # # axes[row, col].set_xticks([1, 2, 3, 4])
    # x = range(1, 5)
    # axes[row, col].set_xticks(x)
    # labels = ['$', '$$', '$$$', '$$$$']
    # labels = [1,2,3,4]
    # axes[row, col].set_xticklabels(['$%.lf$' % y for y in labels])

  fig7.savefig('/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/yelp/static/plots/correlations.png', dpi=200)
  plt.show()


def KDEs(data):
  def kde_sklearn(x, x_grid, bandwidth=0.2, **kwargs):
    """Kernel Density Estimation with Scikit-learn"""
    kde_skl = KernelDensity(bandwidth=bandwidth, **kwargs, kernel='gaussian')
    kde_skl.fit(x[:, np.newaxis])
    # score_samples() returns the log-likelihood of the samples
    log_pdf = kde_skl.score_samples(x_grid[:, np.newaxis])
    return np.exp(log_pdf)
  #TRY KDE WITH DIFFERENT BANDWITHS

  dataRestaurants = data[data['category'] == 'restaurants']
  dataBars = data[data['category'] == 'bars']
  dataCoffee = data[data['category'] == 'coffee']
  dataBeauty = data[data['category'] == 'beautysvc']
  dataGiftshop = data[data['category'] == 'giftshops']

  dataRestaurants['Price'] = dataRestaurants['query_price']
  dataBars['Price'] = dataBars['query_price']
  dataCoffee['Price'] = dataCoffee['query_price']
  dataBeauty['Price'] = dataBeauty['query_price']
  dataGiftshop['Price'] = dataGiftshop['query_price']
  data['Price'] = data['query_price']

  dataRestaurants['Rating'] = dataRestaurants['rating']
  dataBars['Rating'] = dataBars['rating']
  dataCoffee['Rating'] = dataCoffee['rating']
  dataBeauty['Rating'] = dataBeauty['rating']
  dataGiftshop['Rating'] = dataGiftshop['rating']
  data['Rating'] = data['rating']

  x_grid = np.linspace(0, 6, 70)
  datasets = [dataRestaurants, dataBars, dataCoffee, dataBeauty, dataGiftshop, data,
    dataRestaurants, dataBars, dataCoffee, dataBeauty, dataGiftshop, data]
  plots = ['Rating','Rating','Rating','Rating','Rating','Rating',
    'Price','Price','Price','Price','Price','Price']
  rows = [0,1,2,3,4,5,0,1,2,3,4,5] #from left to right= 1-4-5-2-3-6
  cols = [0,0,0,0,0,0,1,1,1,1,1,1]

  titles = ['RATING','','','','','','PRICE','','','','','']
  ts = ['Restaurants', 'Bars', 'Coffee & Tea', 'Beauty & Spas', 'Giftshops', 'All Categories',
    'Restaurants', 'Bars', 'Coffee & Tea', 'Beauty & Spas', 'Giftshops', 'All Categories']

  labels = ['Mode', 'Median']
  fig8, ax = plt.subplots(nrows=6, ncols=2, figsize=(10,10), dpi = 100)
  fig8.suptitle('Kernel Density Estimations of Rating and Price Variables Across Categories',
    fontsize=14)

  for row, col, title, t, dataset, plot in zip(rows, cols, titles, ts, datasets, plots):
    mean = dataset[plot].mean()
    median = dataset[plot].median()
    (_, idx, counts) = np.unique(dataset[plot], return_index=True, return_counts=True)
    index = idx[np.argmax(counts)]
    mode = dataset[plot].iloc[index]
    standardDev = np.std(dataset[plot])
    medianSkewness =  (3 * (mean - median)) / standardDev #P = (3 * (X - Med))/s Pearson’s Median Skewness Coefficient
    modeSkewness =  (mean - mode) / standardDev #P = (3 * (X - Med))/s Pearson’s Median Skewness Coefficient

    ax[row, col].plot(x_grid, kde_sklearn(dataset[plot], x_grid, bandwidth=0.4),
               label='Mode skewness={:2.1f}'.format(modeSkewness), linewidth=3, alpha=0.5) #label='bw={0}'.format(bandwidth),
    ax[row, col].hist(dataset[plot], bins=4, fc='gray', histtype='stepfilled', alpha=0.3, normed=True, label=None)
    if plot == 'Rating':
      ax[row, col].set_xlim(0, 5.5)
    else:
      ax[row, col].set_xlim(0, 4.5)
    # ll1 = ('Mode skewness={:2.1f}'.format(modeSkewness))
    l1 = ax[row, col].axvline(mean, color='b', linestyle='-', linewidth=1) #label='Mean:{:2.1f}'.format(mean)
    l2 = ax[row, col].axvline(median, color='r', linestyle='--', linewidth=1) #label='Median:{:2.1f}'.format(median)
    # print(modeSkewness, medianSkewness)
    ax[row, col].text(.5,1.3, title, weight='heavy', horizontalalignment='center', fontsize=13, transform=ax[row, col].transAxes)
    l3 = ax[row, col].axvline(mode, color='g', linestyle='-.', linewidth=1) #label='Mode:{:2.1f}'.format(mode)
    ax[row, col].legend(loc=0, fontsize=8)
    ax[row, col].set_yticklabels('')
    ax[row, col].yaxis.set_ticks_position('none')
    ax[row, col].set_yticklabels('')
    ax[row, col].set_ylabel(t, rotation=90)
    # ax[row, col].set_title(t, fontsize=10)
  fig8.legend((l1, l2, l3), ('Mean', 'Median', 'Mode'), loc = 'lower center')
  # fig8.legend((l1,), ('Mean',), loc =(4))
  # fig8.legend((l2,), ('Median',), loc = (5))
  # fig8.legend((l3,), ('Mode',), loc = (3))

  fig8.savefig('/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/yelp/static/plots/KDEs.png', dpi=200)
  plt.show()



data = ImportData()
# Stats(data)
# CategoryHeatmaps(data)
Histograms(data)
# JointPlots(data)
# Correlations(data)
# KDEs(data)

#8 plots -- number 5 might be unnecessary


    # ax.text(3, 8, 'boxed italics text in data coords', style='italic',
    #     bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})
  # x_grid = np.linspace(0, 3, 100)
  # x = dataBars['closest2Distance'].dropna()

  # fig, ax = plt.subplots()
  # for bandwidth in [0.1, 0.3, 1.0]:
  #     ax.plot(x_grid, kde_sklearn(x, x_grid, bandwidth=bandwidth),
  #             label='bw={0}'.format(bandwidth), linewidth=3, alpha=0.5)
  # ax.hist(x, 300, fc='gray', histtype='stepfilled', alpha=0.3, normed=True)
  # ax.set_xlim(0, 3)
  # ax.legend(loc='upper right')

  # FIND THE OPTIMUM BANDWIDTH: https://jakevdp.github.io/blog/2013/12/01/kernel-density-estimation/
  # from sklearn.grid_search import GridSearchCV
  # grid = GridSearchCV(KernelDensity(kernel='gaussian'),
  #                     {'bandwidth': np.linspace(0.01, 1.0, 30)},
  #                     cv=20) # 20-fold cross-validation
  # grid.fit(x[:, None])
  # print(grid.best_params_) #{'bandwidth': 0.10000000000000001}


#BUNUNLA IC ICE PLOT YAPMAYI DENE
# grid_kws = {"height_ratios": (.9, .05), "hspace": .3}
# f, (ax, cbar_ax) = plt.subplots(2, gridspec_kw=grid_kws)
# ax = sns.heatmap(flights, ax=ax,
#   cbar_ax=cbar_ax,
#   cbar_kws={"orientation": "horizontal"})
#
  #

  #axes[2].set_xlim([0,60])
# xlim=xlim, ylim=ylim









#  data = data[data['category'] != 'food']
  # data = data[data['category'] != 'nightlife']
  # dataAxes1 = data.pivot_table(values='query_price', index='rating', columns='category')
  # dataAxes2 = data.pivot_table(values='rating', index='query_price', columns='category')
  # # print(deneme)

  # fig1 = plt.figure()

  # axes1 = sns.heatmap(dataAxes1.dropna(), cmap='coolwarm', linecolor='white', linewidths=1, annot=True,
  #   xticklabels=['Bars', 'Beauty & Spas', 'Coffee & Tea', 'Giftshops', 'Restaurants'],
  #   cbar_kws={'label': 'Price'})
  # axes1 = fig1.add_axes([0.1, 0.1, 0.8, 0.8])
  # axes1.set_ylabel('Rating')
  # axes1.set_xlabel('')
  # axes1.set_title('Rating-Price Relationship Across Categories')

  # # Only y-axis labels need their rotation set, x-axis labels already have a rotation of 0
  # _, labels = plt.yticks()
  # plt.setp(labels, rotation=0)

  # fig2 = plt.figure(figsize=(10,10))
  # axes2 = sns.heatmap(dataAxes2.dropna(), cmap='coolwarm', linecolor='white', linewidths=1, annot=True,
  #   xticklabels=['Bars', 'Beauty & Spas', 'Coffee & Tea', 'Giftshops', 'Restaurants'],
  #   cbar_kws={'label': 'Rating'})
  # axes2 = fig2.add_axes([0.1, 0.1, 0.8, 0.8])
  # axes2.set_ylabel('Price')
  # axes2.set_xlabel('')
  # axes2.set_title('Price-Rating Relationship Across Categories')

  # # Only y-axis labels need their rotation set, x-axis labels already have a rotation of 0
  # _, labels = plt.yticks()
  # plt.setp(labels, rotation=0)



# "boundaries": np.linspace(-1, 1, 4)


#SBPLOTS:

# data = range(1,10);
# fig = figure()
# for i in range(6):
#     ax = fig.add_subplot(2,3,i)

#     ax.text(.5,.9,'centered title',
#         horizontalalignment='center',
#         transform=ax.transAxes)

#     ax.plot(data)
# show()


# TIC ON AXES:
# plt.tick_params(
#     axis='x',          # changes apply to the x-axis
#     which='both',      # both major and minor ticks are affected
#     bottom='off',      # ticks along the bottom edge are off
#     top='off',         # ticks along the top edge are off
#     labelbottom='off') # labels along the bottom edge are off
