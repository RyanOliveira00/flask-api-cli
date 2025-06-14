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
import { RootStackParamList, Purchase } from '../types';
import ApiService from '../services/api';

type PurchaseHistoryScreenNavigationProp = StackNavigationProp<RootStackParamList, 'PurchaseHistory'>;

interface Props {
  navigation: PurchaseHistoryScreenNavigationProp;
}

const PurchaseHistoryScreen: React.FC<Props> = ({ navigation }) => {
  const [purchases, setPurchases] = useState<Purchase[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);

  const fetchPurchases = useCallback(async () => {
    try {
      setIsLoading(true);
      const data = await ApiService.getPurchaseHistory();
      setPurchases(data);
    } catch (error: any) {
      Alert.alert('Erro', 'Não foi possível carregar o histórico de compras');
      console.error('Error fetching purchases:', error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const onRefresh = useCallback(async () => {
    setIsRefreshing(true);
    await fetchPurchases();
    setIsRefreshing(false);
  }, [fetchPurchases]);

  useEffect(() => {
    fetchPurchases();
  }, [fetchPurchases]);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const renderPurchaseItem = ({ item }: { item: Purchase }) => (
    <View style={styles.purchaseCard}>
      <View style={styles.purchaseHeader}>
        <Text style={styles.purchaseId}>Compra #{item.id}</Text>
        <Text style={styles.purchaseDate}>{formatDate(item.created_at)}</Text>
      </View>
      
      <View style={styles.purchaseDetails}>
        <Text style={styles.coffeeName}>
          {item.coffee?.name || `Café ID: ${item.coffee_id}`}
        </Text>
        {item.coffee?.description && (
          <Text style={styles.coffeeDescription}>{item.coffee.description}</Text>
        )}
        <Text style={styles.quantity}>Quantidade: {item.quantity}</Text>
        <Text style={styles.totalPrice}>Total: R$ {item.total_price.toFixed(2)}</Text>
      </View>
    </View>
  );

  if (isLoading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#8B4513" />
        <Text style={styles.loadingText}>Carregando histórico...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => navigation.goBack()}
        >
          <Text style={styles.backButtonText}>← Voltar</Text>
        </TouchableOpacity>
        <Text style={styles.title}>Histórico de Compras</Text>
      </View>

      <FlatList
        data={purchases}
        keyExtractor={(item) => item.id.toString()}
        renderItem={renderPurchaseItem}
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
            <Text style={styles.emptyText}>Nenhuma compra realizada ainda</Text>
            <Text style={styles.emptySubText}>
              Suas compras aparecerão aqui após serem realizadas
            </Text>
          </View>
        }
      />

      {purchases.length > 0 && (
        <View style={styles.summary}>
          <Text style={styles.summaryText}>
            Total de compras: {purchases.length}
          </Text>
          <Text style={styles.summaryText}>
            Valor total gasto: R$ {purchases.reduce((total, purchase) => total + purchase.total_price, 0).toFixed(2)}
          </Text>
        </View>
      )}
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
  listContainer: {
    padding: 20,
  },
  purchaseCard: {
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 15,
    marginBottom: 15,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  purchaseHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
    paddingBottom: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  purchaseId: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
  purchaseDate: {
    fontSize: 14,
    color: '#666',
  },
  purchaseDetails: {
    marginTop: 5,
  },
  coffeeName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#8B4513',
    marginBottom: 5,
  },
  coffeeDescription: {
    fontSize: 14,
    color: '#666',
    marginBottom: 5,
  },
  quantity: {
    fontSize: 14,
    color: '#666',
    marginBottom: 5,
  },
  totalPrice: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#4CAF50',
  },
  emptyContainer: {
    alignItems: 'center',
    marginTop: 50,
    paddingHorizontal: 20,
  },
  emptyText: {
    fontSize: 18,
    color: '#666',
    marginBottom: 10,
    textAlign: 'center',
  },
  emptySubText: {
    fontSize: 14,
    color: '#999',
    textAlign: 'center',
  },
  summary: {
    backgroundColor: '#fff',
    padding: 20,
    borderTopWidth: 1,
    borderTopColor: '#ddd',
  },
  summaryText: {
    fontSize: 16,
    color: '#333',
    marginBottom: 5,
    textAlign: 'center',
  },
});

export default PurchaseHistoryScreen; 