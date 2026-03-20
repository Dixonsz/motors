export interface Template {
    id: string;
    title: string;
    content: string;
}

export interface FormField {
    name: string;
    label: string;
    type: 'text' | 'email' | 'password' | 'select' | 'textarea' | 'button';
    required?: boolean;
    options?: string[];
}

export interface TableColumn {
    header: string;
    field: string;
}

export interface Alert {
    message: string;
    type: 'success' | 'error' | 'warning' | 'info';
}

export interface User {
    id: string;
    name: string;
    email: string;
}

export interface Product {
    id: string;
    name: string;
    price: number;
}