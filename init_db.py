from database import init_db, add_sample_data, add_sample_admin

if __name__ == '__main__':
    init_db()
    add_sample_data()
    add_sample_admin()
    print('Database initialized and sample data added.')
