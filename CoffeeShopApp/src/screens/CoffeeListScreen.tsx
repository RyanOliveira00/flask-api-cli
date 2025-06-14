import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  StyleSheet,
  Alert,
  ActivityIndicator,
  RefreshControl,
} from 'react-native';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList, Coffee } from '../types';
import { useAuth } from '../contexts/AuthContext';
import ApiService from '../services/api';

type CoffeeListScreenNavigationProp = StackNavigationProp<RootStackParamList, 'CoffeeList'>;

interface Props {
  navigation: CoffeeListScreenNavigationProp;
}

const CoffeeListScreen: React.FC<Props> = ({ navigation }) => {
  const [coffees, setCoffees] = useState<Coffee[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const { user, logout } = useAuth();

  const fetchCoffees = useCallback(async () => {
    try {
      setIsLoading(true);
      const data = await ApiService.getCoffees();
      setCoffees(data);
    } catch (error: any) {
      Alert.alert('Erro', 'Não foi possível carregar os cafés');
      console.error('Error fetching coffees:', error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const onRefresh = useCallback(async () => {
    setIsRefreshing(true);
    await fetchCoffees();
    setIsRefreshing(false);
  }, [fetchCoffees]);

  useEffect(() => {
    const unsubscribe = navigation.addListener('focus', () => {
      fetchCoffees();
    });

    return unsubscribe;
  }, [navigation, fetchCoffees]);

  const handleBuyCoffee = async (coffee: Coffee) => {
    Alert.alert(
      'Comprar Café',
      `Deseja comprar ${coffee.name} por R$ ${coffee.price.toFixed(2)}?`,
      [
        { text: 'Cancelar', style: 'cancel' },
        { text: 'Comprar', onPress: () => processPurchase(coffee) },
      ]
    );
  };

  const processPurchase = async (coffee: Coffee) => {
    try {
      await ApiService.createPurchase({
        coffee_id: coffee.id,
        quantity: 1,
      });
      Alert.alert('Sucesso', 'Compra realizada com sucesso!');
      fetchCoffees();
    } catch (error: any) {
      Alert.alert('Erro', error.response?.data?.error || 'Erro ao realizar compra');
    }
  };

  const handleEditCoffee = (coffee: Coffee) => {
    navigation.navigate('EditCoffee', { coffee });
  };

  const handleDeleteCoffee = async (coffee: Coffee) => {
    Alert.alert(
      'Excluir Café',
      `Tem certeza que deseja excluir "${coffee.name}"?`,
      [
        { text: 'Cancelar', style: 'cancel' },
        { text: 'Excluir', style: 'destructive', onPress: () => deleteCoffee(coffee.id) },
      ]
    );
  };

  const deleteCoffee = async (coffeeId: number) => {
    try {
      await ApiService.deleteCoffee(coffeeId);
      Alert.alert('Sucesso', 'Café excluído com sucesso!');
      fetchCoffees();
    } catch (error: any) {
      Alert.alert('Erro', error.response?.data?.error || 'Erro ao excluir café');
    }
  };

  const navigateToAddCoffee = () => {
    navigation.navigate('AddCoffee');
  };

  const navigateToPurchaseHistory = () => {
    navigation.navigate('PurchaseHistory');
  };

  const handleLogout = () => {
    Alert.alert(
      'Sair',
      'Tem certeza que deseja sair?',
      [
        { text: 'Cancelar', style: 'cancel' },
        { text: 'Sair', style: 'destructive', onPress: logout },
      ]
    );
  };

  const renderCoffeeItem = ({ item }: { item: Coffee }) => (
    <View style={styles.coffeeCard}>
      <View style={styles.coffeeInfo}>
        <Text style={styles.coffeeName}>{item.name}</Text>
        <Text style={styles.coffeeDescription}>{item.description}</Text>
        <Text style={styles.coffeePrice}>R$ {item.price.toFixed(2)}</Text>
        <Text style={styles.coffeeStock}>Estoque: {item.stock}</Text>
      </View>
      
      <View style={styles.coffeeActions}>
        <TouchableOpacity
          style={[styles.actionButton, styles.buyButton]}
          onPress={() => handleBuyCoffee(item)}
          disabled={item.stock === 0}
        >
          <Text style={styles.buttonText}>
            {item.stock === 0 ? 'Esgotado' : 'Comprar'}
          </Text>
        </TouchableOpacity>
        
        {user?.is_admin && (
          <>
            <TouchableOpacity
              style={[styles.actionButton, styles.editButton]}
              onPress={() => handleEditCoffee(item)}
            >
              <Text style={styles.buttonText}>Editar</Text>
            </TouchableOpacity>
            
            <TouchableOpacity
              style={[styles.actionButton, styles.deleteButton]}
              onPress={() => handleDeleteCoffee(item)}
            >
              <Text style={styles.buttonText}>Excluir</Text>
            </TouchableOpacity>
          </>
        )}
      </View>
    </View>
  );

  if (isLoading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#8B4513" />
        <Text style={styles.loadingText}>Carregando cafés...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>☕ Cafés Disponíveis</Text>
        <View style={styles.headerButtons}>
          <TouchableOpacity
            style={styles.headerButton}
            onPress={navigateToPurchaseHistory}
          >
            <Text style={styles.headerButtonText}>Histórico</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.headerButton}
            onPress={handleLogout}
          >
            <Text style={styles.headerButtonText}>Sair</Text>
          </TouchableOpacity>
        </View>
      </View>

      {user?.is_admin && (
        <TouchableOpacity
          style={styles.addButton}
          onPress={navigateToAddCoffee}
        >
          <Text style={styles.addButtonText}>+ Adicionar Café</Text>
        </TouchableOpacity>
      )}

      <FlatList
        data={coffees}
        keyExtractor={(item) => item.id.toString()}
        renderItem={renderCoffeeItem}
        contentContainerStyle={styles.listContainer}
        refreshControl={
          <RefreshControl
            refreshing={isRefreshing}
            onRefresh={onRefresh}
            colors={['#8B4513']}
          />
        }
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyText}>Nenhum café disponível</Text>
          </View>
        }
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
    color: '#666',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#ddd',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#8B4513',
  },
  headerButtons: {
    flexDirection: 'row',
  },
  headerButton: {
    marginLeft: 10,
    paddingHorizontal: 12,
    paddingVertical: 6,
    backgroundColor: '#8B4513',
    borderRadius: 6,
  },
  headerButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
  },
  addButton: {
    margin: 20,
    padding: 15,
    backgroundColor: '#8B4513',
    borderRadius: 10,
    alignItems: 'center',
  },
  addButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  listContainer: {
    padding: 20,
  },
  coffeeCard: {
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 15,
    marginBottom: 15,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  coffeeInfo: {
    marginBottom: 15,
  },
  coffeeName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  coffeeDescription: {
    fontSize: 14,
    color: '#666',
    marginBottom: 5,
  },
  coffeePrice: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#8B4513',
    marginBottom: 5,
  },
  coffeeStock: {
    fontSize: 14,
    color: '#666',
  },
  coffeeActions: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  actionButton: {
    flex: 1,
    padding: 10,
    borderRadius: 8,
    alignItems: 'center',
    marginHorizontal: 2,
  },
  buyButton: {
    backgroundColor: '#4CAF50',
  },
  editButton: {
    backgroundColor: '#2196F3',
  },
  deleteButton: {
    backgroundColor: '#f44336',
  },
  buttonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
  },
  emptyContainer: {
    alignItems: 'center',
    marginTop: 50,
  },
  emptyText: {
    fontSize: 16,
    color: '#666',
  },
});

export default CoffeeListScreen; 