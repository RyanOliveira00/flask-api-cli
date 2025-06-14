import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
} from 'react-native';
import { StackNavigationProp } from '@react-navigation/stack';
import { RouteProp } from '@react-navigation/native';
import { RootStackParamList } from '../types';
import ApiService from '../services/api';

type EditCoffeeScreenNavigationProp = StackNavigationProp<RootStackParamList, 'EditCoffee'>;
type EditCoffeeScreenRouteProp = RouteProp<RootStackParamList, 'EditCoffee'>;

interface Props {
  navigation: EditCoffeeScreenNavigationProp;
  route: EditCoffeeScreenRouteProp;
}

const EditCoffeeScreen: React.FC<Props> = ({ navigation, route }) => {
  const { coffee } = route.params;
  
  const [name, setName] = useState(coffee.name);
  const [description, setDescription] = useState(coffee.description);
  const [price, setPrice] = useState(coffee.price.toString());
  const [stock, setStock] = useState(coffee.stock.toString());
  const [isLoading, setIsLoading] = useState(false);

  const validateForm = () => {
    if (!name.trim() || !description.trim() || !price.trim() || !stock.trim()) {
      Alert.alert('Erro', 'Por favor, preencha todos os campos');
      return false;
    }

    const priceNum = parseFloat(price);
    const stockNum = parseInt(stock);

    if (isNaN(priceNum) || priceNum <= 0) {
      Alert.alert('Erro', 'Por favor, insira um preço válido');
      return false;
    }

    if (isNaN(stockNum) || stockNum < 0) {
      Alert.alert('Erro', 'Por favor, insira um estoque válido');
      return false;
    }

    return true;
  };

  const handleUpdateCoffee = async () => {
    if (!validateForm()) {
      return;
    }

    try {
      setIsLoading(true);
      await ApiService.updateCoffee(coffee.id, {
        name: name.trim(),
        description: description.trim(),
        price: parseFloat(price),
        stock: parseInt(stock),
      });
      
      Alert.alert('Sucesso', 'Café atualizado com sucesso!', [
        { text: 'OK', onPress: () => navigation.goBack() },
      ]);
    } catch (error: any) {
      Alert.alert('Erro', error.response?.data?.error || 'Erro ao atualizar café');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.header}>
          <TouchableOpacity
            style={styles.backButton}
            onPress={() => navigation.goBack()}
          >
            <Text style={styles.backButtonText}>← Voltar</Text>
          </TouchableOpacity>
          <Text style={styles.title}>Editar Café</Text>
        </View>

        <View style={styles.form}>
          <Text style={styles.label}>Nome do Café</Text>
          <TextInput
            style={styles.input}
            placeholder="Ex: Espresso, Cappuccino"
            value={name}
            onChangeText={setName}
            autoCapitalize="words"
          />

          <Text style={styles.label}>Descrição</Text>
          <TextInput
            style={[styles.input, styles.textArea]}
            placeholder="Descreva o café..."
            value={description}
            onChangeText={setDescription}
            multiline
            numberOfLines={3}
            textAlignVertical="top"
          />

          <Text style={styles.label}>Preço (R$)</Text>
          <TextInput
            style={styles.input}
            placeholder="Ex: 4.50"
            value={price}
            onChangeText={setPrice}
            keyboardType="decimal-pad"
          />

          <Text style={styles.label}>Estoque</Text>
          <TextInput
            style={styles.input}
            placeholder="Ex: 100"
            value={stock}
            onChangeText={setStock}
            keyboardType="number-pad"
          />

          <TouchableOpacity
            style={[styles.button, isLoading && styles.buttonDisabled]}
            onPress={handleUpdateCoffee}
            disabled={isLoading}
          >
            {isLoading ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <Text style={styles.buttonText}>Atualizar Café</Text>
            )}
          </TouchableOpacity>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  scrollContent: {
    flexGrow: 1,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#ddd',
  },
  backButton: {
    marginRight: 15,
  },
  backButtonText: {
    fontSize: 16,
    color: '#8B4513',
    fontWeight: 'bold',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#8B4513',
  },
  form: {
    padding: 20,
  },
  label: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 8,
    marginTop: 15,
  },
  input: {
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 15,
    fontSize: 16,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  textArea: {
    height: 80,
  },
  button: {
    backgroundColor: '#8B4513',
    borderRadius: 10,
    padding: 15,
    alignItems: 'center',
    marginTop: 30,
  },
  buttonDisabled: {
    opacity: 0.7,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

export default EditCoffeeScreen; 