<pre>
1. Xác định các Resources trong miền (Domain Resources)
    Dựa vào mô tả bài toán, các danh từ chính (resources) trong hệ thống gồm:   
    users: Người dùng / Tác giả.   
    profiles / profile: Hồ sơ người dùng.   
    posts: Bài viết.   
    comments: Bình luận trong bài viết.   
    tags: Thẻ phân loại bài viết.   
    followers / following: Quan hệ theo dõi giữa các user.   
2. Phân loại Collection
    Collection:         
        /api/v1/posts       GET (lấy DS bài viết), POST (tạo bài viết mới)
        /api/v1/users       GET (lấy DS người dùng), POST (đăng ký user mới)
        /api/v1/tags        GET (lấy DS các thẻ tag)
    Item (Singleton):   
        /api/v1/posts/{id}  GET, PUT, PATCH, DELETE (tác động lên 1 bài viết)
        /api/v1/users/{id}  GET, PUT, PATCH, DELETE (tác động lên 1 user)
        /api/v1/users/me    GET, PATCH (hồ sơ của user đang đăng nhập -  Current Actor)
    Sub-resource:
        /api/v1/posts/{id}/comments     GET (lấy bình luận của post), POST (thêm bình luận)
        /api/v1/posts/{id}/comments/{comment_id}    GET, DELETE (bình luận cụ thể)
        /api/v1/users/{id}/followers    GET, POST / DELETE (follow/unfollow)
        /api/v1/posts/{id}/tags         GET (danh sách tag của post), PUT (gắn tag)


3. Sơ đồ cây Endpoint (Endpoint Tree Chart)
Sử dụng Version segment /api/v1 ở gốc:  
/api/v1
│
├── /users
│   ├── /{user_id}
│   │   ├── /followers             (Collection sub-resource)
│   │   │   └── /{follower_id}     (Item sub-resource)
│   │   └── /following
│   └── /me                        (Singular current actor)
│
├── /posts
│   ├── /{post_id}
│   │   ├── /comments              (Collection sub-resource)
│   │   │   └── /{comment_id}      (Item sub-resource)
│   │   └── /tags                  (Sub-resource)
│   └── ?tag={tag_slug}&author_id={id} (Filter collection)
│
└── /tags
    └── /{tag_id}


4. Triển khai Flask Routes cho Collection (trong file app.py)
    <pre>



