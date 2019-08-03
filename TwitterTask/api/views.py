import requests
import urllib3
from bs4 import BeautifulSoup
from rest_framework.response import Response
from rest_framework.views import APIView


class getUserTweets(APIView):
    def get(self, request,user):
        try:
            limit = 30
            if request.GET.get('limit'):
                limit = int(request.GET['limit'])
            tweet_data = scrap_tweets(user, limit)
        except:
            return Response({'Tweets': []})
        return Response(tweet_data)


def scrap_tweets(user, limit):
        res = requests.get('https://twitter.com/' + user)
        bs = BeautifulSoup(res.content, 'lxml')

        all_tweets = bs.find_all('div', {'class': 'tweet'})
        tweet_data = []
        if all_tweets:
            for tweet in all_tweets[:limit]:
                # context = tweet.find('div', {'class': 'context'}).text.replace("\n", " ").strip()
                content = tweet.find('div', {'class': 'content'})
                header = content.find('div', {'class': 'stream-item-header'})
                user = header.find('a', {
                    'class': 'account-group js-account-group js-action-profile js-user-profile-link js-nav'}).text.replace(
                    "\n", " ").strip()
                id = header.find('a', {'class': 'tweet-timestamp js-permalink js-nav js-tooltip'}).attrs
                tweet_id = id.get('data-conversation-id')
                time = id.get('title')
                href = id.get('href')
                message = content.find('div', {'class': 'js-tweet-text-container'}).text.replace("\n", " ").strip()
                footer = content.find('div', {'class': 'stream-item-footer'})
                stat = footer.find('div', {'class': 'ProfileTweet-actionCountList u-hiddenVisually'}).text.replace("\n",
                                                                                                                   " ").strip()
                data = stat.split(' ')
                replies = data[0]
                retweets = data[6]
                likes = data[12]

                tweet_data.append(
                    {"account": {"fullname": user,
                                 "href": href,
                                 "id": tweet_id},
                     "date": time,
                     "likes": likes,
                     "replies": replies,
                     "retweets": retweets,
                     "text": message
                     }
                )

            return tweet_data


        else:
            return tweet_data


class getHashTagsTweet(APIView):
    def get(self,request, hashtag):
        try:
            limit = 30
            if request.GET.get('limit'):
                limit = int(request.GET.get('limit'))
            hash_tag_tweets = tweets_by_hashtag(hashtag, limit)
        except:
            return Response([])
        return Response(hash_tag_tweets)


def tweets_by_hashtag(hashtag, limit):
    http_handler = urllib3.PoolManager()

    tweeter_url = 'https://twitter.com/hashtag/'+ hashtag + '?src=hash'
    print(tweeter_url)
    page = http_handler.request('GET', tweeter_url)

    soup = BeautifulSoup(page.data, 'html')
    all_tweets = list()
    for index, tweet_html in enumerate(soup.find_all('li', attrs={'data-item-type': 'tweet'})):
        if limit > 0 and index == limit - 1:
            break

        all_tweets.append({
            'account': {
                'fullname': tweet_html.find('strong', attrs={'class': 'fullname'}).text,
                'href': 'https://twitter.com/' + tweet_html.find('a', attrs={'class': 'account-group'})['href'],
                'id': tweet_html.find('a', attrs={'class': 'account-group'})['data-user-id'],
            },
            'date': tweet_html.find('small', attrs={'class': 'time'}).a['title'],
            'hashtags': ['#' + hashtag.b.text for hashtag in
                         tweet_html.find_all('a', attrs={'class': 'twitter-hashtag'})],
            'likes': int(tweet_html.find('div', attrs={'class': 'ProfileTweet-action--favorite'}).button.find('span',
                                                                                                              attrs={
                                                                                                                  'class': 'ProfileTweet-actionCount'}).span.text or 0),
            'replies': int(tweet_html.find('div', attrs={'class': 'ProfileTweet-action--reply'}).button.find('span',
                                                                                                             attrs={
                                                                                                                 'class': 'ProfileTweet-actionCount'}).span.text or 0),
            'retweets': int(tweet_html.find('div', attrs={'class': 'ProfileTweet-action--retweet'}).button.find('span',
                                                                                                                attrs={
                                                                                                                    'class': 'ProfileTweet-actionCount'}).span.text or 0),
            'text': tweet_html.find('div', attrs={'class': 'js-tweet-text-container'}).p.text
        })


    return all_tweets
