from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, Category
from .forms import ImageUploadForm, ProductForm, RegistrationForm, LoginForm
import torch
from torch import nn
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import numpy as np
import cv2

# resnedi load etmeli
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = models.efficientnet_b7(pretrained=True)
model = nn.Sequential(*(list(model.children())[:-1]))  # Remove the classifier layer
model = model.to(device)
model.eval()

# Suratlary model kabul eder valy etmeli
# Giriş ululygyny EfficientNet-B7 bilen gabat getirmek üçin täze preprocess pipeline döredýäris
preprocess = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((600, 600)),  # EfficientNet-B7 üçin laýyk ululyk
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def extract_features(image):
    input_tensor = preprocess(image).unsqueeze(0).to(device)
    
    with torch.no_grad(): 
        features = model(input_tensor)
    
    # netijedakileri 1 olcegli matris gecirmeli
    return features.flatten().cpu().numpy().astype(np.float32)

def deep_similarity_check(img1, img2):
    features1 = extract_features(img1)
    features2 = extract_features(img2)

    # menzeshliklerini tapmaly
    similarity = np.dot(features1, features2) / (np.linalg.norm(features1) * np.linalg.norm(features2))
    
    return similarity

def find_similar_products(reference_image):
    products = Product.objects.exclude(features__isnull=True)
    similar_products = []

    # netijedakileri image owuryas
    reference_features = extract_features(reference_image)

    # Menzeshlikleri boynuca sortirowka
    for product in products:
        # DB-dan okap almaly
        product_features = np.frombuffer(product.features, dtype=np.float32)
        
        # menzeshlik bahalaryny hasapla
        if len(reference_features) == len(product_features):
            score = np.dot(reference_features, product_features) / (np.linalg.norm(reference_features) * np.linalg.norm(product_features))
            similar_products.append((product, score))

    # menzeshlik bahalary boynuca duzmek
    similar_products.sort(key=lambda x: x[1], reverse=True)

    return similar_products

def image_search(request):
    if request.method == 'POST':
        uploaded_image = request.FILES['image']
        
    
        img = Image.open(uploaded_image)
        img_array = np.array(img)
    
        reference_image = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

        similar_products = find_similar_products(reference_image)

        if similar_products:
            return render(request, 'search/results.html', {'similar_products': similar_products})
        else:
            return render(request, 'search/no_results.html')
    
    return render(request, 'search/upload.html')
def product_list(request):
    category_id = request.GET.get('category')
    categories = Category.objects.all()
    if category_id:
        products = Product.objects.filter(category_id=category_id)
        selected_category = get_object_or_404(Category, id=category_id)
    else:
        products = Product.objects.all()
        selected_category = None
        
    return render(request, 'search/product_list.html', {
        'products': products, 
        'categories': categories,
        'selected_category': selected_category
    })

def home(request):
    categories = Category.objects.all()
    return render(request, 'search/home.html', {'categories': categories})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('add_product')
    else:
        form = ProductForm()
    
    categories = Category.objects.all()
    return render(request, 'product/add_product.html', {'form': form, 'categories': categories})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product/product_detail.html', {'product': product})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('product_list')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')
