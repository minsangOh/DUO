from locust import HttpUser, task, between

class SampleUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        print('test start')

    @task
    def product_recommendations_deposit(self):
        self.client.get("accounts/recommend_products_save/1/")
        
    @task
    def savings_recommendations_save(self):
        self.client.get("accounts/recommend_products_save/1/")

