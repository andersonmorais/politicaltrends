#PoliticalTrends

This Application allows you to get an overall Political Insight from published texts/articles which contains politics context.
The App makes use of IBM Watson AlchemyAPI to extract semantic information about key persons and to obtain the respective subjective opinion from the identified politician.

## Publish the App on Bluemix using CF CLI

1. Download and install the [Cloud-foundry CLI][cloud_foundry] tool

2. Connect to Bluemix in the command line tool
  ```sh
  $ cf api https://api.ng.bluemix.net
  $ cf login -u <your user ID>
  ```

3. Create the MongoDB Databse Service on Bluemix

  ```sh
  $ cf create-service mongodb "100" mongodb1"
  ```

4. Publish the app on Bluemix.

  ```sh
  $ git clone https://github.com/andersonmorais/politicaltrends.git
  $ cd politicaltrends
  $ cf push  --no-start
  ```

5. Start the app.

  ```sh
  $ cf start politicaltrends
  ```
  
6. Check the app at:

  ```sh
  http://politicaltrends.mybluemix.net/
  ```

[cloud_foundry]: https://github.com/cloudfoundry/cli
[getting_started]: https://console.ng.bluemix.net/solutions/web-applications
