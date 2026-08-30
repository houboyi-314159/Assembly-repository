#!/usr/bin/env python3
"""
hash_calculator.py - 文件哈希计算工具（支持多种算法）
"""

import hashlib
import os
import sys
from pathlib import Path
import time
from typing import Dict, Tuple, Optional
import argparse

class FileHasher:
    """文件哈希计算器"""
    
    # 支持的哈希算法及其说明
    ALGORITHMS = {
        'md5': 'MD5 (128位) - 快速，用于文件完整性校验',
        'sha1': 'SHA-1 (160位) - 已被证实不安全，不推荐用于安全用途',
        'sha224': 'SHA-224 (224位) - SHA-2系列',
        'sha256': 'SHA-256 (256位) - 最常用，安全可靠',
        'sha384': 'SHA-384 (384位) - SHA-2系列',
        'sha512': 'SHA-512 (512位) - 最高安全级别',
        'sha3_224': 'SHA3-224 (224位) - SHA-3系列',
        'sha3_256': 'SHA3-256 (256位) - SHA-3系列',
        'sha3_384': 'SHA3-384 (384位) - SHA-3系列',
        'sha3_512': 'SHA3-512 (512位) - SHA-3系列',
        'blake2b': 'BLAKE2b (512位) - 高性能',
        'blake2s': 'BLAKE2s (256位) - 适用于32位系统',
        'sha512_224': 'SHA-512/224 (224位)',
        'sha512_256': 'SHA-512/256 (256位)',
    }
    
    @classmethod
    def list_algorithms(cls) -> Dict[str, str]:
        """列出所有可用算法"""
        available = {}
        for algo, description in cls.ALGORITHMS.items():
            if algo in hashlib.algorithms_available:
                available[algo] = description
        return available
    
    @staticmethod
    def calculate_hash(file_path: str, algorithm: str = 'sha256', 
                      chunk_size: int = 8192) -> Tuple[Optional[str], float]:
        """
        计算文件哈希值
        
        Args:
            file_path: 文件路径
            algorithm: 哈希算法
            chunk_size: 分块大小（字节）
            
        Returns:
            (哈希值, 耗时秒数) 或 (None, 0) 如果出错
        """
        if algorithm not in hashlib.algorithms_available:
            return None, 0
        
        try:
            start_time = time.time()
            hasher = hashlib.new(algorithm)
            
            with open(file_path, 'rb') as f:
                while chunk := f.read(chunk_size):
                    hasher.update(chunk)
            
            elapsed = time.time() - start_time
            return hasher.hexdigest(), elapsed
            
        except Exception as e:
            print(f"错误: {e}")
            return None, 0
    
    @staticmethod
    def calculate_multiple_hashes(file_path: str, algorithms: list, 
                                chunk_size: int = 8192) -> Dict[str, str]:
        """一次性计算多种哈希值"""
        results = {}
        
        # 初始化所有哈希器
        hashers = {}
        for algo in algorithms:
            if algo in hashlib.algorithms_available:
                hashers[algo] = hashlib.new(algo)
            else:
                print(f"警告: 算法 {algo} 不可用")
        
        if not hashers:
            return results
        
        # 一次性读取文件并更新所有哈希器
        try:
            with open(file_path, 'rb') as f:
                while chunk := f.read(chunk_size):
                    for hasher in hashers.values():
                        hasher.update(chunk)
            
            # 获取所有哈希结果
            for algo, hasher in hashers.items():
                results[algo] = hasher.hexdigest()
                
        except Exception as e:
            print(f"错误: {e}")
        
        return results

def print_hash_result(file_path: str, hash_value: str, algorithm: str, 
                     elapsed: float, file_size: int = None):
    """格式化输出哈希结果"""
    print("\n" + "="*60)
    print(f"文件: {file_path}")
    if file_size:
        print(f"大小: {file_size:,} 字节 ({file_size/1024:.2f} KB)")
    print(f"算法: {algorithm.upper()}")
    print(f"哈希值: {hash_value}")
    print(f"耗时: {elapsed:.3f} 秒")
    
    # 计算速度
    if elapsed > 0 and file_size:
        speed = file_size / elapsed / 1024 / 1024  # MB/s
        print(f"速度: {speed:.2f} MB/s")
    print("="*60)

def interactive_mode():
    """交互式模式"""
    hasher = FileHasher()
    
    while True:
        print("\n" + "="*60)
        print("文件哈希计算工具")
        print("="*60)
        
        # 列出可用算法
        print("\n可用哈希算法:")
        available = hasher.list_algorithms()
        for i, (algo, desc) in enumerate(available.items(), 1):
            print(f"  {i:2d}. {algo:<12} - {desc}")
        
        print("\n操作选项:")
        print("  1. 计算单个文件哈希")
        print("  2. 批量计算文件哈希")
        print("  3. 验证文件哈希")
        print("  4. 比较两个文件")
        print("  5. 退出")
        
        choice = input("\n请选择操作 (1-5): ").strip()
        
        if choice == '1':
            # 单个文件计算
            file_path = input("请输入文件路径: ").strip()
            if not os.path.exists(file_path):
                print(f"错误: 文件不存在 '{file_path}'")
                continue
            
            print("\n可用算法:")
            for i, (algo, _) in enumerate(available.items(), 1):
                print(f"  {i}. {algo}")
            print("  a. 所有算法")
            
            algo_choice = input("请选择算法 (编号/名称 或 'a' 计算所有): ").strip().lower()
            
            file_size = os.path.getsize(file_path)
            
            if algo_choice == 'a':
                # 计算所有算法
                print(f"\n计算 {file_path} 的所有哈希值...")
                results = hasher.calculate_multiple_hashes(
                    file_path, list(available.keys()))
                
                for algo, hash_val in results.items():
                    print(f"\n{algo.upper():<12}: {hash_val}")
            
            else:
                # 计算单个算法
                if algo_choice.isdigit():
                    idx = int(algo_choice) - 1
                    if 0 <= idx < len(available):
                        algorithm = list(available.keys())[idx]
                    else:
                        print("错误: 无效的选择")
                        continue
                else:
                    algorithm = algo_choice
                
                if algorithm not in available:
                    print(f"错误: 不支持的算法 '{algorithm}'")
                    continue
                
                print(f"\n正在计算 {algorithm.upper()} 哈希值...")
                hash_value, elapsed = hasher.calculate_hash(file_path, algorithm)
                
                if hash_value:
                    print_hash_result(file_path, hash_value, algorithm, elapsed, file_size)
                    
                    # 询问是否保存结果
                    save = input("\n是否保存结果到文件? (y/N): ").strip().lower()
                    if save == 'y':
                        with open(f"{file_path}.{algorithm}.txt", 'w') as f:
                            f.write(f"{algorithm.upper()}: {hash_value}\n")
                            f.write(f"File: {file_path}\n")
                            f.write(f"Size: {file_size} bytes\n")
                        print(f"结果已保存到 {file_path}.{algorithm}.txt")
        
        elif choice == '2':
            # 批量计算
            directory = input("请输入目录路径: ").strip()
            if not os.path.isdir(directory):
                print(f"错误: 目录不存在 '{directory}'")
                continue
            
            algorithm = input("请输入哈希算法 (默认sha256): ").strip() or 'sha256'
            if algorithm not in available:
                print(f"错误: 不支持的算法 '{algorithm}'")
                continue
            
            ext_filter = input("请输入文件扩展名过滤 (如 .txt .pdf, 留空为所有): ").strip()
            extensions = [ext.strip() for ext in ext_filter.split()] if ext_filter else None
            
            output_file = input("请输入输出文件名 (留空不保存): ").strip()
            
            print(f"\n正在批量计算 {algorithm.upper()} 哈希值...")
            
            results = []
            for filepath in Path(directory).rglob('*'):
                if filepath.is_file():
                    if extensions and filepath.suffix.lower() not in extensions:
                        continue
                    
                    print(f"处理: {filepath}")
                    hash_value, elapsed = hasher.calculate_hash(str(filepath), algorithm)
                    
                    if hash_value:
                        results.append({
                            'file': str(filepath),
                            'hash': hash_value,
                            'size': filepath.stat().st_size
                        })
            
            # 输出结果
            print(f"\n批量计算完成，共 {len(results)} 个文件")
            for item in results:
                print(f"{item['hash']}  {item['file']}")
            
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    for item in results:
                        f.write(f"{item['hash']}  {item['file']}\n")
                print(f"结果已保存到 {output_file}")
        
        elif choice == '3':
            # 验证哈希
            file_path = input("请输入文件路径: ").strip()
            if not os.path.exists(file_path):
                print(f"错误: 文件不存在 '{file_path}'")
                continue
            
            algorithm = input("请输入哈希算法 (默认sha256): ").strip() or 'sha256'
            expected_hash = input("请输入期望的哈希值: ").strip()
            
            print(f"\n正在验证 {algorithm.upper()} 哈希值...")
            hash_value, elapsed = hasher.calculate_hash(file_path, algorithm)
            
            if hash_value:
                matches = hash_value.lower() == expected_hash.lower()
                print_hash_result(file_path, hash_value, algorithm, elapsed)
                
                if matches:
                    print("✅ 哈希验证通过！")
                else:
                    print("❌ 哈希验证失败！")
                    print(f"期望: {expected_hash}")
        
        elif choice == '4':
            # 比较两个文件
            file1 = input("请输入第一个文件路径: ").strip()
            file2 = input("请输入第二个文件路径: ").strip()
            
            if not (os.path.exists(file1) and os.path.exists(file2)):
                print("错误: 文件不存在")
                continue
            
            algorithm = input("请输入哈希算法 (默认sha256): ").strip() or 'sha256'
            
            print(f"\n正在比较文件...")
            hash1, _ = hasher.calculate_hash(file1, algorithm)
            hash2, _ = hasher.calculate_hash(file2, algorithm)
            
            if hash1 and hash2:
                print(f"\n文件1 ({file1}):")
                print(f"  {algorithm.upper()}: {hash1}")
                print(f"\n文件2 ({file2}):")
                print(f"  {algorithm.upper()}: {hash2}")
                
                if hash1 == hash2:
                    print(f"\n✅ 两个文件完全相同")
                else:
                    print(f"\n❌ 两个文件不同")
        
        elif choice == '5':
            print("再见！")
            break
        
        else:
            print("无效的选择，请重试")

def command_line_mode():
    """命令行模式"""
    parser = argparse.ArgumentParser(
        description='计算文件哈希值（支持多种算法）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s file.txt                    # 使用默认SHA256计算
  %(prog)s file.txt -a md5            # 使用MD5计算
  %(prog)s file.txt -a all            # 使用所有算法计算
  %(prog)s dir/ -r -a sha256          # 递归计算目录
  %(prog)s file.txt -c expected_hash  # 验证哈希
  %(prog)s -l                         # 列出可用算法
        """
    )
    
    parser.add_argument('path', nargs='?', help='文件或目录路径')
    parser.add_argument('-a', '--algorithm', default='sha256', 
                       help='哈希算法 (使用 -l 查看所有)')
    parser.add_argument('-r', '--recursive', action='store_true',
                       help='递归处理目录')
    parser.add_argument('-c', '--check', metavar='HASH',
                       help='验证文件哈希值')
    parser.add_argument('-l', '--list', action='store_true',
                       help='列出所有可用算法')
    parser.add_argument('-o', '--output', 
                       help='保存结果到文件')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='显示详细信息')
    
    args = parser.parse_args()
    
    hasher = FileHasher()
    
    if args.list:
        print("可用的哈希算法:")
        for algo, desc in hasher.list_algorithms().items():
            print(f"  {algo:<12} - {desc}")
        return
    
    if not args.path:
        parser.print_help()
        return
    
    if args.algorithm.lower() == 'all':
        algorithms = list(hasher.list_algorithms().keys())
    else:
        if args.algorithm not in hasher.list_algorithms():
            print(f"错误: 不支持的算法 '{args.algorithm}'")
            print("使用 -l 查看可用算法")
            return
        algorithms = [args.algorithm]
    
    if os.path.isfile(args.path):
        # 处理单个文件
        for algo in algorithms:
            hash_value, elapsed = hasher.calculate_hash(args.path, algo)
            if hash_value:
                print(f"{algo.upper()}: {hash_value}")
                
                if args.verbose:
                    file_size = os.path.getsize(args.path)
                    print(f"文件: {args.path}")
                    print(f"大小: {file_size:,} 字节")
                    print(f"耗时: {elapsed:.3f} 秒")
                
                if args.check:
                    if hash_value.lower() == args.check.lower():
                        print(f"✅ {algo.upper()} 验证通过")
                    else:
                        print(f"❌ {algo.upper()} 验证失败")
                        print(f"   期望: {args.check}")
                        print(f"   实际: {hash_value}")
    
    elif os.path.isdir(args.path) and args.recursive:
        # 递归处理目录
        results = []
        for filepath in Path(args.path).rglob('*'):
            if filepath.is_file():
                for algo in algorithms:
                    hash_value, _ = hasher.calculate_hash(str(filepath), algo)
                    if hash_value:
                        results.append(f"{hash_value}  {filepath}")
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write('\n'.join(results))
            print(f"结果已保存到 {args.output}")
        else:
            for line in results:
                print(line)
    
    else:
        print(f"错误: 路径不存在或不是文件: {args.path}")
        print("使用 -r 递归处理目录")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 命令行模式
        command_line_mode()
    else:
        # 交互式模式
        try:
            interactive_mode()
        except KeyboardInterrupt:
            print("\n\n程序被用户中断")
        except Exception as e:
            print(f"错误: {e}")