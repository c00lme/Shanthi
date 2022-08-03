const NaturalLanguageUnderstandingV1 = require('ibm-watson/natural-language-understanding/v1');
const { IamAuthenticator } = require('ibm-watson/auth');
const csv = require('csv-parser')
const fs = require('fs')




//bro wats the api key 




const naturalLanguageUnderstanding = new NaturalLanguageUnderstandingV1({
    version: '2019-07-12',
    authenticator: new IamAuthenticator({
        apikey: 'YOUR_API_KEY'
    }),
    url: 'https://gateway.watsonplatform.net/natural-language-understanding/api'
});

naturalLanguageUnderstanding.authenticate().then(() => {
    console.log('authenticated');
}
).catch(err => {
    console.log(err);
}
);


const descriptions = []
fs.createReadStream('csvjson.json')
    .pipe(csv())
    .on('data', (data) => {
        descriptions.push(data.description)
    }
    )
    .on('end', () => {
        console.log(descriptions)
    }    
    )
    .on('error', (err) => {
        console.log(err.message)
    }
    )


    const happinessScores = []
    descriptions.forEach(description => {
        naturalLanguageUnderstanding.analyze({   
            text: description,
            features: {
                sentiment: {}
            }
        })
        .then(analysisResults => {
            happinessScores.push(analysisResults.result.sentiment.document.score)
        }
        )
        .catch(err => {
            console.log(err)
        }
        )
    }
    )
    console.log(happinessScores)













    

    







