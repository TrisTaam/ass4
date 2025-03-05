class AppDatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'customer':
            return 'default'  # Changed from 'customers'
        elif model._meta.app_label == 'items':
            return 'items'
        elif model._meta.app_label in ['cart', 'order', 'shipping', 'paying']:
            return 'transactions'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'customer':
            return 'default'  # Changed from 'customers'
        elif model._meta.app_label == 'items':
            return 'items'
        elif model._meta.app_label in ['cart', 'order', 'shipping', 'paying']:
            return 'transactions'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        db1 = self.db_for_read(obj1.__class__)
        db2 = self.db_for_read(obj2.__class__)
        return db1 == db2

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'customer':
            return db == 'default'  # Changed from 'customers'
        elif app_label == 'items':
            return db == 'items'
        elif app_label in ['cart', 'order', 'shipping', 'paying']:
            return db == 'transactions'
        else:
            return db == 'default'