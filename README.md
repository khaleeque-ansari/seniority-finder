# Seniority Finder

Given User profile consisting of education and experience, we need to find out his seniority. 
I have focused more on the coding part rather than improving accuracy of classifier
 
## Getting Started



1. Clone the directory

2. Install requirements.txt
 
3. Update the root path in "configs/__init__.py"

3. Run "classifier/seniority_random_forest.py" to find seniority


## Further Improvements

### Improvements
#### - add more comments
#### - add proper logging before sending to production, Use logging.Logger
#### - in Logger also log which version of model is running (store model_id)
#### - Normalizing the data, data enrichment for both degrees and titles
#### - Do clustering for both degrees and titles
#### - Add classes for each component
#### - Keep logging production results(query,predicted) , so that we can keep track of performance.

#### - Test Cases for parsers(eduction_parser, experience_parser)
#### - Use title and industry to better understand seniority, For e.g. Google VP is very senior compared to Bank's VP which is not very senior
#### - Measure of performance should include deviation from true label, for e.g. manager predicted as director is not very wrong but director predicted as intern is verry wrong
