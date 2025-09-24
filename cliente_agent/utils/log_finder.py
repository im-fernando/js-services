#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Localizador de Logs para Serviços Quality
Implementa navegação automática na estrutura de pastas aninhadas
"""

import os
import glob
from pathlib import Path
from typing import Optional, List, Tuple
import re

class QualityLogFinder:
    """Localizador inteligente de logs para serviços Quality"""
    
    def __init__(self, base_path: str, log_pattern: str = "*.txt"):
        self.base_path = Path(base_path)
        self.log_pattern = log_pattern
    
    def find_latest_log_file(self) -> Optional[str]:
        """
        Navega pela estrutura aninhada e encontra o arquivo de log mais recente
        
        Estrutura esperada:
        C:\Quality\LOG\{service}\{pasta_num}\{pasta_num}\{pasta_num}\{arquivo.txt}
        
        Returns:
            Caminho para o arquivo de log mais recente ou None se não encontrado
        """
        try:
            if not self.base_path.exists():
                return None
            
            current_path = self.base_path
            
            # Navegar pelos 3 níveis de pastas numéricas
            for level in range(3):
                numeric_folders = self._get_numeric_folders(current_path)
                if not numeric_folders:
                    # Se não há pastas numéricas, procurar diretamente por arquivos
                    return self._find_latest_in_directory(current_path)
                
                # Pegar a pasta com o número mais alto (mais recente)
                latest_folder = max(numeric_folders, key=int)
                current_path = current_path / latest_folder
            
            # Encontrar arquivo .txt mais recente na pasta final
            return self._find_latest_in_directory(current_path)
            
        except Exception as e:
            print(f"❌ Erro ao localizar logs em {self.base_path}: {e}")
            return None
    
    def _get_numeric_folders(self, path: Path) -> List[str]:
        """
        Retorna lista de pastas que contêm apenas números
        
        Args:
            path: Caminho para verificar
            
        Returns:
            Lista de nomes de pastas numéricas
        """
        try:
            if not path.exists() or not path.is_dir():
                return []
            
            numeric_folders = []
            for item in path.iterdir():
                if item.is_dir() and item.name.isdigit():
                    numeric_folders.append(item.name)
            
            return sorted(numeric_folders)
            
        except Exception:
            return []
    
    def _find_latest_in_directory(self, path: Path) -> Optional[str]:
        """
        Encontra o arquivo de log mais recente em um diretório
        
        Args:
            path: Diretório para procurar
            
        Returns:
            Caminho para o arquivo mais recente ou None
        """
        try:
            if not path.exists():
                return None
            
            # Procurar por arquivos que correspondem ao padrão
            pattern = str(path / self.log_pattern)
            txt_files = glob.glob(pattern)
            
            if not txt_files:
                return None
            
            # Retornar o arquivo com timestamp mais recente
            latest_file = max(txt_files, key=os.path.getmtime)
            return latest_file
            
        except Exception:
            return None
    
    def get_log_files_by_date(self, days_back: int = 7) -> List[Tuple[str, float]]:
        """
        Retorna lista de arquivos de log dos últimos N dias
        
        Args:
            days_back: Número de dias para buscar
            
        Returns:
            Lista de tuplas (caminho_arquivo, timestamp_modificacao)
        """
        import time
        from datetime import datetime, timedelta
        
        cutoff_time = time.time() - (days_back * 24 * 60 * 60)
        log_files = []
        
        try:
            # Buscar recursivamente por arquivos de log
            for root, dirs, files in os.walk(self.base_path):
                for file in files:
                    if file.endswith('.txt'):
                        file_path = os.path.join(root, file)
                        mod_time = os.path.getmtime(file_path)
                        
                        if mod_time >= cutoff_time:
                            log_files.append((file_path, mod_time))
            
            # Ordenar por timestamp (mais recente primeiro)
            log_files.sort(key=lambda x: x[1], reverse=True)
            return log_files
            
        except Exception as e:
            print(f"❌ Erro ao buscar logs por data: {e}")
            return []
    
    def get_log_structure_info(self) -> dict:
        """
        Retorna informações sobre a estrutura de logs
        
        Returns:
            Dicionário com informações da estrutura
        """
        info = {
            'base_path': str(self.base_path),
            'exists': self.base_path.exists(),
            'levels': [],
            'total_files': 0,
            'latest_file': None
        }
        
        try:
            if not self.base_path.exists():
                return info
            
            current_path = self.base_path
            
            # Analisar cada nível
            for level in range(3):
                numeric_folders = self._get_numeric_folders(current_path)
                if not numeric_folders:
                    break
                
                level_info = {
                    'level': level + 1,
                    'path': str(current_path),
                    'numeric_folders': numeric_folders,
                    'latest_folder': max(numeric_folders, key=int) if numeric_folders else None
                }
                info['levels'].append(level_info)
                
                # Avançar para o próximo nível
                if numeric_folders:
                    latest_folder = max(numeric_folders, key=int)
                    current_path = current_path / latest_folder
            
            # Contar arquivos totais
            info['total_files'] = len(glob.glob(str(current_path / self.log_pattern)))
            info['latest_file'] = self.find_latest_log_file()
            
        except Exception as e:
            info['error'] = str(e)
        
        return info

def test_log_finder():
    """Função de teste para o log finder"""
    print("🧪 Testando QualityLogFinder...")
    
    # Teste com caminho de exemplo
    test_path = "C:\\Quality\\LOG\\Integra"
    finder = QualityLogFinder(test_path)
    
    print(f"📁 Testando caminho: {test_path}")
    
    # Informações da estrutura
    info = finder.get_log_structure_info()
    print(f"📊 Estrutura encontrada: {info}")
    
    # Arquivo mais recente
    latest = finder.find_latest_log_file()
    print(f"📄 Arquivo mais recente: {latest}")
    
    # Arquivos dos últimos 7 dias
    recent_files = finder.get_log_files_by_date(7)
    print(f"📅 Arquivos dos últimos 7 dias: {len(recent_files)}")

if __name__ == "__main__":
    test_log_finder()
