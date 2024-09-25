# THINK OF A NAME FOR THIS
John Bedette, 2024
### A better walkability score for my homesearch

## Concept
#### Problem:
I'm looking for a new house. I live in Portland. 
I like how I can walk to several different clusters of good bars, cafes, and restaurants.
I want to move out to a more suburban location.
I want to be able to walk places that are cool.

This idea of a walkability score is not new, I just haven't found one that factors in a sense of taste.
I'm not looking for easy walking to a stripmall full of bad food and safeway.

#### Goal:
I want to make my own walkability browser extension that will:
- work with redfin or zillow to grab addresses
- be able to just be given an address and also provide the same data
- provide an walkability rating that doesn't just say you can walk to the cvs and pf chang's

#### Needs:
1. A mapping Api, going with google to start
2. additional government datasets for development, zoning and crime
3. some sort of integration wtih redfin or zillow listings, hopefully just lift address when clicking on listing
4. an extension page with the walkability analysis, if feels cumbersome to overlay it on the page or something
    
    
## Current Roadmap:
### Phase 1, Get data.
#### Summary: Mapping api, extra data sets, correctness of data
1. get basic google maps api working for different poi types 
    - we're gonna be doing stuff with maps, make sure maps is working how i think it should
2. get access to local data sets about devolopment and crime stats.
    - i've found some promising data, seems like i might not be able to access it from europe.

#### Phase 2, Analyze findings
##### Summary: Refine searches, combine and analyze
1. Add more walkability analysis from google maps data, the easy bits:
    want to know if there exists within walking distance:
        - is there public transport
        - is there a greenway for bikes etc
        - is there a decent park
        - is there a grocery store
2. analysis of goodstuff cluster: is there a decent cluster of shops and restaurants?
    - how to exclude strip malls
    - how to get all food establishements, seems like my initial attempts aren't getting all restaurants/bars/foodcarts.
    - some way of taking ratings
        - yelp, google maps ratings, and trip advisor all suck. Maybe in tandem I could get something.
        - maybe eater has something, usually are pretty on-point.
        - might be able to leverage ml somehow, kind of a vague thing that ml might be good for analysis
3. make system to analyze development and crime stats.
    - google maps has tons of analytics, but the government data coming in needs my own analysis metrics

### Phase 3, browser extension
#### Summary: Put this into a browser extension
1. make browser extenstion that can take in an address and display findnigs on a browser tab.
2. have browser extension automatically get address from zillow and refin navigation

## 